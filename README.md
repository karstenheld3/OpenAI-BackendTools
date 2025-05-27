# OpenAI-BackendTools
A collection of tools and demo code to test, operate and maintain Open AI and Azure OpenAI backends.

- **Authentication Management**: Support for multiple authentication methods including Service Principals, Managed Identities, and API Keys
- **File Operations**: Tools for listing files used in vector stores and assistants with storage metrics.
- **Cleanup Operations**: Tools for deleting expired and unused files to save cost.
- **RAG Operations**: Code that demonstrates uploading files to vector stores with metadata extraction.
- **Vector Store Search**: Code that demonstrates vector store search, filtering and query reqwrite.

The toolkit is targeted at developers and operators who need to interact with Azure OpenAI services programmatically.

[Azure OpenAI documentation](AzureOpenAI.md)
- Creating your .env file and where to get the information from
- Example .env files for access via API keys, Managed Identity, and Service Principal
- Azure Open AI deployment and access types
- How to set up access roles for managed identities and service principals
- Terminology explained: What is a service principal, managed identity, tenant, client ID, client secret


## Open AI Links

| Source                          | Links                                                        |                                                              |                                                              |                                                              |                                                              |
| ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Open AI Docs                    | [Models](https://platform.openai.com/docs/models)            | [Pricing](https://platform.openai.com/docs/pricing)          | [Cookbook](https://cookbook.openai.com/)                     | [Assistants](https://platform.openai.com/docs/assistants/overview) | [Agents](https://platform.openai.com/docs/guides/agents)     |
| Open AI Docs                    | [Built-In tools](https://platform.openai.com/docs/guides/agents) | [Evals](https://platform.openai.com/docs/guides/evals)       | [Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning) | [Retrieval / Search](https://platform.openai.com/docs/guides/retrieval) | [Actions](https://platform.openai.com/docs/actions/introduction) |
| Open AI Docs                    | [Data retention](https://platform.openai.com/docs/guides/your-data) |                                                              |                                                              |                                                              |                                                              |
| Open AI Docs - File search tool | [File search tool](https://platform.openai.com/docs/guides/tools-file-search) | [Retrieval customization](https://platform.openai.com/docs/guides/tools-file-search#retrieval-customization) | [Metadata filtering](https://platform.openai.com/docs/guides/tools-file-search#metadata-filtering) | [Supported files](https://platform.openai.com/docs/guides/tools-file-search#supported-files) |                                                              |
| Open AI API                     | [Responses](https://platform.openai.com/docs/api-reference/responses) | [Completions](https://platform.openai.com/docs/api-reference/chat) | [Files](https://platform.openai.com/docs/api-reference/files) | [Vector stores](https://platform.openai.com/docs/api-reference/vector-stores) | [Assistants](https://platform.openai.com/docs/api-reference/assistants) |
| Open AI Python                  | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) |                                                              |                                                              |                                                              |                                                              |

### Requirements / Packages
- azure-identity 1.23.0 ([releases](https://pypi.org/project/azure-identity/))
- requests 2.32.3 ([releases](https://pypi.org/project/requests/))
- python-dotenv 1.1.0 ([releases](https://pypi.org/project/python-dotenv/))
- openai version 1.79.0 ([releases](https://github.com/openai/openai-python/tags))

### Files
- files_tool.py

