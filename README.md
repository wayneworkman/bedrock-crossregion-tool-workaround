# AWS Bedrock Cross-Region Tool Workaround

Created by [Wayne Workman](https://github.com/wayneworkman)

[![Blog](https://img.shields.io/badge/Blog-wayne.theworkmans.us-blue)](https://wayne.theworkmans.us/)
[![GitHub](https://img.shields.io/badge/GitHub-wayneworkman-181717?logo=github)](https://github.com/wayneworkman)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wayne_Workman-0077B5?logo=linkedin)](https://www.linkedin.com/in/wayne-workman-a8b37b353/)
[![SpinnyLights](https://img.shields.io/badge/SpinnyLights-wayneworkman-764ba2)](https://spinnylights.com/wayneworkman)

This Terraform module deploys an AWS Lambda function that uses Amazon Bedrock to detect prompt injection attempts in user input. The module implements the security principles outlined in [this hands-on demo](https://wayne.theworkmans.us/posts/2025/10/2025-10-18-prompt-injection-hands-on-demo.html).


A practical workaround for the lack of native tool support in AWS Bedrock's cross-region inference profiles. Use prompt engineering to extract code from any model's response, enabling easy model swapping for cost optimization.

## The Problem

AWS Bedrock's Converse API provides a unified interface for different AI models and supports native tool usage - but **not with cross-region inference profiles**. If you want to use cross-region inference (for better availability and reliability), you lose native tool support.

## The Solution

This example demonstrates how to emulate tool usage through prompt engineering. Instead of using the native `toolConfig` parameter, we teach the model to respond in a specific format that we can parse.

## Why This Matters

- **Cost Optimization**: Easily test if cheaper models (Nova Premier) can handle your task before using expensive ones (Claude Opus)
- **Model Agnostic**: Switch between Nova Premier, Claude Sonnet, Claude Opus, or any future model by changing just one line - no code refactoring needed
- **Cross-Region Benefits**: Get improved availability and failover while still having tool-like functionality
- **Simple Implementation**: Under 80 lines of Python

## The Power of Converse API's Unified Interface

Before the Converse API, working with different AI models was a nightmare:
- Each provider (Anthropic, Amazon, Meta) had completely different input/output formats
- Developers needed 100+ lines of complex helper functions for each model
- Switching models meant rewriting significant portions of your code

Now with Converse API:
- **One line change**: Switch between models by changing only `MODEL_ID`
- **Same code, any model**: The exact same code works across all supported models
- **Future-proof**: When new models are released, they'll work with your existing code

Example of switching models:
```python
# Start with the cheapest option
MODEL_ID = 'us.amazon.nova-premier-v1:0'

# Need more capability? Just change this line:
MODEL_ID = 'us.anthropic.claude-opus-4-1-20250805-v1:0'

# That's it! No other code changes needed.
```

## Quick Start

```bash
# Clone the repo
git clone https://github.com/wayneworkman/bedrock-crossregion-tool-workaround.git
cd bedrock-crossregion-tool-workaround

# Ensure AWS credentials are configured (aws configure or IAM role)

# Run the example (region is set in the script to us-east-2)
python3 bedrock_custom_tool_demo.py
```

## How It Works

1. **Prompt Engineering**: We include instructions in the prompt teaching the model to respond with `TOOL: python_executor` followed by a code fence
2. **Model Response**: The model follows the pattern and generates code in the specified format
3. **Code Extraction**: We parse the response using regex to extract the Python code
4. **Execution Ready**: The extracted code can be executed, stored, or processed as needed

## Example Input/Output

**Input Prompt:**
```
Write a Python script that lists all EC2 instances across all regions
```

**Model Response:**
```
TOOL: python_executor
```python
import boto3

def list_all_instances():
    ec2 = boto3.client('ec2')
    # ... generated code ...
```

**Extracted Code:**
```python
import boto3

def list_all_instances():
    ec2 = boto3.client('ec2')
    # ... generated code ...
```

## Supported Models

Tested with these cross-region inference profiles:
- `us.amazon.nova-premier-v1:0` - Cheapest option, great for simple tasks
- `us.anthropic.claude-sonnet-4-20250514-v1:0` - Good balance of cost/capability
- `us.anthropic.claude-opus-4-1-20250805-v1:0` - Most capable but expensive

Just change the `MODEL_ID` constant to switch models:

```python
MODEL_ID = 'us.amazon.nova-premier-v1:0'  # Start cheap
# MODEL_ID = 'us.anthropic.claude-opus-4-1-20250805-v1:0'  # Use when needed
```

## Cost Savings Example

**Token Pricing (AWS Bedrock):**

Nova Premier:
- Input: $0.0025 per 1,000 tokens
- Output: $0.0125 per 1,000 tokens

Claude Opus 4.1:
- Input: $0.015 per 1,000 tokens
- Output: $0.075 per 1,000 tokens

**Typical Code Generation Request (2,000 tokens):**
- **Nova Premier**: ~$0.02
- **Claude Opus 4.1**: ~$0.12
- **Savings**: 6x cheaper with Nova

Test with Nova first, only upgrade to Claude when necessary.

## Limitations

- Not a true replacement for native tool support (when AWS adds it, switch to that)
- Requires careful prompt engineering for consistent results
- Model-dependent reliability (some models follow instructions better)
- No built-in validation of tool format compliance

## Future Improvements

When AWS adds native tool support to cross-region inference:
1. The Converse API calls remain the same
2. Just add the `toolConfig` parameter
3. Remove the prompt engineering instructions
4. Update the response parsing logic

## License

[MIT](./LICENSE)