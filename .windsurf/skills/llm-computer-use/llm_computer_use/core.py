"""Core module - Screen capture, actions, session, and Anthropic provider."""
import os
import time
import base64
import json
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum

class ScreenCapture:
    """Fast screenshot capture with resize for LLM APIs."""
    
    def __init__(self, max_edge: int = 1568, jpeg_quality: int = 85):
        self.max_edge = max_edge
        self.jpeg_quality = jpeg_quality
        self._mss = None
    
    def _get_mss(self):
        if self._mss is None:
            import mss
            self._mss = mss.mss()
        return self._mss
    
    def capture_raw(self, monitor: int = 1):
        """Capture screenshot as PIL Image."""
        from PIL import Image
        sct = self._get_mss()
        screenshot = sct.grab(sct.monitors[monitor])
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    
    def resize_if_needed(self, img):
        """Resize image if larger than max_edge."""
        from PIL import Image
        w, h = img.size
        if w <= self.max_edge and h <= self.max_edge:
            return img
        if w > h:
            new_w = self.max_edge
            new_h = int(h * (self.max_edge / w))
        else:
            new_h = self.max_edge
            new_w = int(w * (self.max_edge / h))
        return img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)
    
    def to_base64(self, img) -> str:
        """Convert PIL Image to JPEG base64 string."""
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=self.jpeg_quality)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    def capture_for_api(self, monitor: int = 1) -> Dict[str, Any]:
        """Capture, resize, and encode - ready for API."""
        start = time.perf_counter()
        img = self.capture_raw(monitor)
        original_size = img.size
        resized = self.resize_if_needed(img)
        b64 = self.to_base64(resized)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return {
            "base64": b64,
            "media_type": "image/jpeg",
            "original_size": original_size,
            "resized_size": resized.size,
            "capture_ms": round(elapsed_ms, 2),
        }
    
    def get_display_info(self) -> Dict[str, Any]:
        """Get display information."""
        sct = self._get_mss()
        monitors = [{"index": i, "width": m["width"], "height": m["height"]} 
                    for i, m in enumerate(sct.monitors)]
        return {"monitor_count": len(monitors) - 1, "monitors": monitors}

class ActionType(Enum):
    SCREENSHOT = "screenshot"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    MIDDLE_CLICK = "middle_click"
    DOUBLE_CLICK = "double_click"
    TRIPLE_CLICK = "triple_click"
    MOUSE_MOVE = "mouse_move"
    SCROLL = "scroll"
    TYPE = "type"
    KEY = "key"
    HOLD_KEY = "hold_key"
    WAIT = "wait"
    LEFT_CLICK_DRAG = "left_click_drag"
    LEFT_MOUSE_DOWN = "left_mouse_down"
    LEFT_MOUSE_UP = "left_mouse_up"

@dataclass
class Action:
    """Represents an action to execute."""
    action_type: ActionType
    coordinate: Optional[Tuple[int, int]] = None
    text: Optional[str] = None
    key: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[int] = None
    duration_seconds: Optional[float] = None
    start_coordinate: Optional[Tuple[int, int]] = None
    end_coordinate: Optional[Tuple[int, int]] = None

@dataclass
class ActionResult:
    """Result of executing an action."""
    success: bool
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0

HIGH_RISK_PATTERNS = ["alt+f4", "ctrl+alt+delete", "del ", "rm ", "format", "shutdown", "reboot"]

def is_high_risk(action: Action) -> bool:
    """Check if action is high-risk."""
    if action.action_type == ActionType.KEY and action.key:
        return any(p in action.key.lower() for p in HIGH_RISK_PATTERNS)
    if action.action_type == ActionType.TYPE and action.text:
        return any(p in action.text.lower() for p in HIGH_RISK_PATTERNS)
    return False

def execute_action(action: Action, dry_run: bool = False) -> ActionResult:
    """Execute a single action."""
    start = time.perf_counter()
    if dry_run:
        return ActionResult(success=True, execution_time_ms=(time.perf_counter() - start) * 1000)
    
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        
        if action.action_type == ActionType.LEFT_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1])
            else:
                pyautogui.click()
        elif action.action_type == ActionType.RIGHT_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1], button='right')
            else:
                pyautogui.click(button='right')
        elif action.action_type == ActionType.MIDDLE_CLICK:
            if action.coordinate:
                pyautogui.click(action.coordinate[0], action.coordinate[1], button='middle')
            else:
                pyautogui.click(button='middle')
        elif action.action_type == ActionType.DOUBLE_CLICK:
            if action.coordinate:
                pyautogui.doubleClick(action.coordinate[0], action.coordinate[1])
            else:
                pyautogui.doubleClick()
        elif action.action_type == ActionType.TRIPLE_CLICK:
            if action.coordinate:
                pyautogui.tripleClick(action.coordinate[0], action.coordinate[1])
            else:
                pyautogui.tripleClick()
        elif action.action_type == ActionType.MOUSE_MOVE:
            if action.coordinate:
                pyautogui.moveTo(action.coordinate[0], action.coordinate[1])
        elif action.action_type == ActionType.SCROLL:
            amount = action.amount or 3
            x, y = action.coordinate if action.coordinate else (None, None)
            if action.direction == "up":
                pyautogui.scroll(amount, x, y)
            elif action.direction == "down":
                pyautogui.scroll(-amount, x, y)
        elif action.action_type == ActionType.TYPE:
            if action.text:
                pyautogui.write(action.text, interval=0.02)
        elif action.action_type == ActionType.KEY:
            if action.key:
                pyautogui.hotkey(*action.key.lower().split('+'))
        elif action.action_type == ActionType.HOLD_KEY:
            if action.key and action.duration_seconds:
                pyautogui.keyDown(action.key.lower())
                time.sleep(action.duration_seconds)
                pyautogui.keyUp(action.key.lower())
        elif action.action_type == ActionType.WAIT:
            if action.duration_seconds:
                time.sleep(action.duration_seconds)
        elif action.action_type == ActionType.LEFT_MOUSE_DOWN:
            if action.coordinate:
                pyautogui.moveTo(action.coordinate[0], action.coordinate[1])
            pyautogui.mouseDown(button='left')
        elif action.action_type == ActionType.LEFT_MOUSE_UP:
            if action.coordinate:
                pyautogui.moveTo(action.coordinate[0], action.coordinate[1])
            pyautogui.mouseUp(button='left')
        elif action.action_type == ActionType.LEFT_CLICK_DRAG:
            if action.start_coordinate and action.end_coordinate:
                pyautogui.moveTo(action.start_coordinate[0], action.start_coordinate[1])
                pyautogui.drag(
                    action.end_coordinate[0] - action.start_coordinate[0],
                    action.end_coordinate[1] - action.start_coordinate[1]
                )
        
        return ActionResult(success=True, execution_time_ms=(time.perf_counter() - start) * 1000)
    except Exception as e:
        return ActionResult(success=False, error_message=str(e), execution_time_ms=(time.perf_counter() - start) * 1000)

def parse_anthropic_action(tool_input: Dict[str, Any]) -> Action:
    """Parse Anthropic tool_use input into Action."""
    action_str = tool_input.get("action", "screenshot")
    try:
        action_type = ActionType(action_str)
    except ValueError:
        action_type = ActionType.SCREENSHOT
    
    coordinate = None
    if "coordinate" in tool_input:
        c = tool_input["coordinate"]
        coordinate = (int(c[0]), int(c[1]))
    
    start_coord = None
    if "start_coordinate" in tool_input:
        c = tool_input["start_coordinate"]
        start_coord = (int(c[0]), int(c[1]))
    
    end_coord = None
    if "end_coordinate" in tool_input:
        c = tool_input["end_coordinate"]
        end_coord = (int(c[0]), int(c[1]))
    
    return Action(
        action_type=action_type,
        coordinate=coordinate,
        text=tool_input.get("text"),
        key=tool_input.get("key"),
        direction=tool_input.get("direction"),
        amount=tool_input.get("amount"),
        duration_seconds=tool_input.get("duration_seconds"),
        start_coordinate=start_coord,
        end_coordinate=end_coord,
    )

class AnthropicProvider:
    """Anthropic Computer Use API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5",
                 max_tokens: int = 1024, display_width: int = 1568, display_height: int = 980):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        self.display_width = display_width
        self.display_height = display_height
        self._client = None
        self.tool_version = "computer_20250124"
        self.beta_flag = "computer-use-2025-01-24"
    
    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key, timeout=60.0, max_retries=2)
        return self._client
    
    def _build_tools(self) -> List[Dict[str, Any]]:
        return [{"type": self.tool_version, "name": "computer",
                 "display_width_px": self.display_width, "display_height_px": self.display_height, "display_number": 1}]
    
    def send_message(self, messages: List[Dict[str, Any]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Send message to API."""
        client = self._get_client()
        kwargs = {"model": self.model, "max_tokens": self.max_tokens, "tools": self._build_tools(),
                  "messages": messages, "betas": [self.beta_flag]}
        if system_prompt:
            kwargs["system"] = system_prompt
        
        start = time.perf_counter()
        response = client.beta.messages.create(**kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        return {"id": response.id, "content": response.content, "stop_reason": response.stop_reason,
                "usage": {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens},
                "latency_ms": round(elapsed_ms, 2)}
    
    def create_user_message(self, text: str, screenshot_base64: Optional[str] = None) -> Dict[str, Any]:
        """Create user message with optional screenshot."""
        content = []
        if screenshot_base64:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": screenshot_base64}})
        content.append({"type": "text", "text": text})
        return {"role": "user", "content": content}
    
    def create_tool_result(self, tool_use_id: str, screenshot_base64: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
        """Create tool result message."""
        content = []
        if error:
            content.append({"type": "text", "text": f"Error: {error}"})
        elif screenshot_base64:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": screenshot_base64}})
        return {"type": "tool_result", "tool_use_id": tool_use_id,
                "content": content if content else [{"type": "text", "text": "Action completed"}]}
    
    def extract_actions(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tool_use blocks from response."""
        actions = []
        for block in response.get("content", []):
            if hasattr(block, "type") and block.type == "tool_use":
                actions.append({"id": block.id, "name": block.name, "input": block.input})
            elif isinstance(block, dict) and block.get("type") == "tool_use":
                actions.append({"id": block["id"], "name": block["name"], "input": block["input"]})
        return actions
    
    def extract_text(self, response: Dict[str, Any]) -> str:
        """Extract text from response."""
        texts = []
        for block in response.get("content", []):
            if hasattr(block, "type") and block.type == "text":
                texts.append(block.text)
            elif isinstance(block, dict) and block.get("type") == "text":
                texts.append(block["text"])
        return "\n".join(texts)

class SessionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    MAX_ITERATIONS = "max_iterations_reached"

@dataclass
class AgentSession:
    """Manages an automation session."""
    
    task_prompt: str
    max_iterations: int = 10
    dry_run: bool = True
    model: str = "claude-sonnet-4-5"
    
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    status: SessionStatus = SessionStatus.PENDING
    current_iteration: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_api_latency_ms: float = 0.0
    start_time: datetime = field(default=None)
    end_time: datetime = field(default=None)
    actions_log: List[Dict[str, Any]] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    
    _screen_capture: ScreenCapture = field(default=None, repr=False)
    _provider: AnthropicProvider = field(default=None, repr=False)
    _confirm_callback: Optional[Callable[[Action], bool]] = field(default=None, repr=False)
    
    def __post_init__(self):
        if self._screen_capture is None:
            self._screen_capture = ScreenCapture()
        if self._provider is None:
            display = self._screen_capture.get_display_info()
            primary = display["monitors"][1] if len(display["monitors"]) > 1 else display["monitors"][0]
            self._provider = AnthropicProvider(model=self.model,
                display_width=min(primary["width"], 1568), display_height=min(primary["height"], 980))
    
    def set_confirm_callback(self, callback: Callable[[Action], bool]):
        self._confirm_callback = callback
    
    def run(self, verbose: bool = True) -> Dict[str, Any]:
        """Run the session."""
        self.status = SessionStatus.RUNNING
        self.start_time = datetime.now()
        
        if verbose:
            print(f"\n{'='*60}\nSession {self.session_id} started")
            print(f"Task: {self.task_prompt[:80]}...\nMax iterations: {self.max_iterations}\nDry run: {self.dry_run}\n{'='*60}\n")
        
        screenshot = self._screen_capture.capture_for_api()
        self.messages.append(self._provider.create_user_message(self.task_prompt, screenshot["base64"]))
        
        while self.current_iteration < self.max_iterations:
            self.current_iteration += 1
            if verbose:
                print(f"\n--- Iteration {self.current_iteration}/{self.max_iterations} ---")
            
            try:
                response = self._provider.send_message(self.messages)
            except Exception as e:
                if verbose:
                    print(f"API Error: {e}")
                self.status = SessionStatus.FAILED
                return self._get_summary(error=str(e))
            
            self.total_input_tokens += response["usage"]["input_tokens"]
            self.total_output_tokens += response["usage"]["output_tokens"]
            self.total_api_latency_ms += response.get("latency_ms", 0)
            
            text_response = self._provider.extract_text(response)
            if text_response and verbose:
                print(f"Model: {text_response[:200]}...")
            
            actions = self._provider.extract_actions(response)
            if not actions:
                if verbose:
                    print("No actions requested - task complete")
                self.status = SessionStatus.COMPLETED
                return self._get_summary()
            
            self.messages.append({"role": "assistant", "content": response["content"]})
            tool_results = []
            
            for action_data in actions:
                action = parse_anthropic_action(action_data["input"])
                if verbose:
                    print(f"Action: {action.action_type.value}", end="")
                    if action.coordinate:
                        print(f" at {action.coordinate}", end="")
                    print()
                
                if action.action_type == ActionType.SCREENSHOT:
                    screenshot = self._screen_capture.capture_for_api()
                    tool_results.append(self._provider.create_tool_result(action_data["id"], screenshot["base64"]))
                    continue
                
                if not self.dry_run and is_high_risk(action):
                    if self._confirm_callback and not self._confirm_callback(action):
                        self.status = SessionStatus.CANCELLED
                        return self._get_summary(error="High-risk action rejected")
                
                result = execute_action(action, dry_run=self.dry_run)
                self.actions_log.append({"iteration": self.current_iteration, "action": action.action_type.value,
                                         "coordinate": action.coordinate, "success": result.success, "dry_run": self.dry_run})
                
                if verbose:
                    print(f"  -> {'OK' if result.success else 'FAIL'} {'(dry-run)' if self.dry_run else ''}")
                
                if not self.dry_run:
                    time.sleep(0.1)
                
                screenshot = self._screen_capture.capture_for_api()
                tool_results.append(self._provider.create_tool_result(action_data["id"],
                    screenshot["base64"] if result.success else None, result.error_message if not result.success else None))
            
            self.messages.append({"role": "user", "content": tool_results})
        
        if verbose:
            print(f"\nMax iterations ({self.max_iterations}) reached")
        self.status = SessionStatus.MAX_ITERATIONS
        return self._get_summary()
    
    def _estimate_cost(self) -> float:
        pricing = {"claude-sonnet-4-5": (3.0, 15.0), "claude-opus-4-5": (15.0, 75.0), "claude-haiku-4-5": (0.80, 4.0)}
        in_rate, out_rate = pricing.get(self.model, (3.0, 15.0))
        return round((self.total_input_tokens / 1_000_000) * in_rate + (self.total_output_tokens / 1_000_000) * out_rate, 6)
    
    def _get_summary(self, error: str = None) -> Dict[str, Any]:
        self.end_time = datetime.now()
        duration_ms = (self.end_time - self.start_time).total_seconds() * 1000 if self.start_time else 0
        return {"session_id": self.session_id, "status": self.status.value, "model": self.model,
                "iterations": self.current_iteration, "max_iterations": self.max_iterations, "dry_run": self.dry_run,
                "total_input_tokens": self.total_input_tokens, "total_output_tokens": self.total_output_tokens,
                "total_api_latency_ms": round(self.total_api_latency_ms, 2), "total_duration_ms": round(duration_ms, 2),
                "actions_count": len(self.actions_log), "estimated_cost_usd": self._estimate_cost(), "error": error}
    
    def save_log(self, path: str = None):
        if path is None:
            path = f"session_{self.session_id}.json"
        with open(path, "w") as f:
            json.dump({"session_id": self.session_id, "task_prompt": self.task_prompt, "status": self.status.value,
                       "iterations": self.current_iteration, "dry_run": self.dry_run,
                       "tokens": {"input": self.total_input_tokens, "output": self.total_output_tokens},
                       "actions": self.actions_log}, f, indent=2)
        return path
