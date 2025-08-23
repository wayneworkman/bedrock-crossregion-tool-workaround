#!/usr/bin/env python3

import boto3
import re

# Configuration
AWS_REGION = 'us-east-2'
MODEL_ID = 'us.amazon.nova-premier-v1:0' # cross-region inference profile for Nova Premier.
# MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0' # cross-region inference prfile for Sonnet 4
# MODEL_ID = 'us.anthropic.claude-opus-4-1-20250805-v1:0' # cross-region inference profile for Opus 4.1 
MAX_TOKENS = 4000
TEMPERATURE = 0.3


def main():
    # Initialize Bedrock client
    bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
    
    # User request
    user_request = "Write a Python script that lists all EC2 instances across all regions with proper pagination handling. Include instance ID, name tag, state, and instance type."
    
    # Create prompt with tool instructions
    prompt = f"""You are an AI assistant with access to execute Python code through a special tool.

TOOL USAGE INSTRUCTIONS:
When you need to execute Python code, you MUST follow this exact format:

1. First line must contain ONLY: TOOL: python_executor
2. Immediately follow with a markdown code fence containing your Python code
3. Do not include any text between the tool declaration and the code fence

Example of correct format:
TOOL: python_executor
```python
import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_instances()
print(response)
```

IMPORTANT RULES:
- The first line of your response must be "TOOL: python_executor" if you want to execute code
- Use only one code fence per response
- After receiving execution results, you can interpret them for the user
- If you don't need to execute code, just respond normally without the TOOL: prefix
- Always use print() statements to output results you want to see

USER REQUEST:
{user_request}"""
    
    # Call Bedrock
    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        inferenceConfig={
            "maxTokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
    )
    
    # Extract response text
    response_text = response['output']['message']['content'][0]['text']
    
    # Extract code from response
    lines = response_text.strip().split('\n')
    if lines[0].strip().upper().startswith('TOOL: PYTHON_EXECUTOR'):
        # Find and extract the code
        code_match = re.search(r'```python\n(.*?)\n```', response_text, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            print(code)

if __name__ == "__main__":
    main()