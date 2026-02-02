# INFO: OpenAI API - SDKs and Libraries

**Doc ID**: OAIAPI-IN15
**Goal**: Document official SDKs and client libraries
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

OpenAI provides official SDKs for Python and Node.js/TypeScript, with community-maintained libraries for other languages. The SDKs provide typed interfaces, automatic retries, streaming support, and simplified authentication. They follow semantic versioning for stability. The Python SDK (`openai`) and Node.js SDK (`openai`) are the primary supported clients, offering full API coverage including Chat Completions, Responses, Assistants, and all Platform APIs.

## Key Facts

- **Python SDK**: `pip install openai` [VERIFIED]
- **Node.js SDK**: `npm install openai` [VERIFIED]
- **Versioning**: Semantic versioning (semver) [VERIFIED]
- **Source**: https://github.com/openai/openai-python, openai-node [VERIFIED]

## Official SDKs

### Python

**Installation**

```bash
pip install openai
```

**Requirements**: Python 3.8+

**Basic Usage**

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

**Features**
- Fully typed with Pydantic models
- Automatic retries with exponential backoff
- Streaming support
- Async client (`AsyncOpenAI`)
- File uploads
- Pagination helpers

**Async Usage**

```python
from openai import AsyncOpenAI
import asyncio

async def main():
    client = AsyncOpenAI()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

**GitHub**: https://github.com/openai/openai-python

### Node.js / TypeScript

**Installation**

```bash
npm install openai
# or
yarn add openai
```

**Requirements**: Node.js 18+

**Basic Usage**

```typescript
import OpenAI from "openai";

const client = new OpenAI();  // Uses OPENAI_API_KEY env var

async function main() {
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello!" }],
  });

  console.log(response.choices[0].message.content);
}

main();
```

**Features**
- Full TypeScript types
- Automatic retries
- Streaming with async iterators
- ESM and CommonJS support
- File uploads
- Pagination helpers

**Streaming**

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function main() {
  const stream = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello!" }],
    stream: true,
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || "");
  }
}

main();
```

**GitHub**: https://github.com/openai/openai-node

## Community Libraries

### .NET / C#

```csharp
// Azure.AI.OpenAI (Microsoft official for Azure OpenAI)
dotnet add package Azure.AI.OpenAI

// OpenAI-DotNet (community)
dotnet add package OpenAI-DotNet
```

### Go

```bash
# Community maintained
go get github.com/sashabaranov/go-openai
```

### Java / Kotlin

```xml
<!-- Community: openai-java -->
<dependency>
    <groupId>com.theokanning.openai-gpt3-java</groupId>
    <artifactId>service</artifactId>
    <version>0.18.0</version>
</dependency>
```

### Ruby

```ruby
# Gemfile
gem "ruby-openai"
```

### PHP

```bash
composer require openai-php/client
```

### Rust

```toml
# Cargo.toml
[dependencies]
async-openai = "0.18"
```

## SDK Configuration

### Python Configuration

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",  # Or use OPENAI_API_KEY env var
    organization="org-...",  # Optional
    project="proj-...",  # Optional
    base_url="https://api.openai.com/v1",  # Default
    timeout=60.0,  # Request timeout
    max_retries=2,  # Automatic retries
)
```

### Node.js Configuration

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: "org-...",
  project: "proj-...",
  baseURL: "https://api.openai.com/v1",
  timeout: 60000,
  maxRetries: 2,
});
```

## Proxy/Custom Base URL

### Azure OpenAI

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://your-resource.openai.azure.com",
    api_key="your-azure-key",
    api_version="2024-02-01"
)
```

### Custom Proxy

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-proxy.example.com/v1"
)
```

## Version Management

```bash
# Install specific version
pip install openai==1.12.0

# Upgrade to latest
pip install --upgrade openai

# Check version
python -c "import openai; print(openai.__version__)"
```

## Related Endpoints

- `_INFO_OAIAPI_INTRODUCTION.md` - API overview
- `_INFO_OAIAPI_AUTHENTICATION.md` - Authentication setup

## Sources

- OAIAPI-IN01-SC-OAI-LIBS - Official libraries documentation

## Document History

**[2026-01-30 09:55]**
- Initial documentation created
