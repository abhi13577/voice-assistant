INTENT_REGISTRY = {
    "greeting": {
    "level": "system",
    "examples": [
        "Hello",
        "Hi",
        "Hey",
        "Help",
        "What can you do",
        "What can you do?",
        "What are your capabilities",
        "How can you help me"
    ]
},
    "check_run_status": {
    "level": "L1",
    "examples": [
        "What's the status of my last run?",
        "How did my run go?",
        "Check my run status",
        "Did my run pass?",
        "How did my last run go?",
        "How did my test run go?",
        "How did my last test run go?",
        "What happened in my last run?",
        "Did my last test run pass?"
    ]
},
    "list_projects": {
    "level": "L1",
    "examples": [
        "List my projects",
        "What projects do I have?",
        "Show my projects"
    ]
},
    "list_runs": {
    "level": "L1",
    "examples": [
        "Show my recent test runs",
        "List my runs"
    ]
},
    "explain_failure": {
        "level": "L1",
        "examples": [
            "Why did my test fail?",
            "Why did it fail?",
            "Explain the last failure",
            "What caused the failure?"
        ]
    },
    "account_usage": {
        "level": "L1",
        "examples": [
            "What is my run limit?",
            "How many runs do I have left?",
            "What is my usage?",
            "Show my test run usage"
        ]
    },
    "rerun_test": {
        "level": "L1",
        "examples": [
            "Rerun this test",
            "Run it again",
            "Can you rerun Checkout Pay with Card?",
            "Queue this test again"
        ]
    },
    "troubleshoot_selector": {
        "level": "L1",
        "examples": [
            "The selector broke",
            "Element not found",
            "Login selector not working",
            "Selector not found error"
        ]
    },
    "troubleshoot_timeout": {
        "level": "L1",
        "examples": [
            "The test timed out",
            "Timeout on pay button",
            "It says timeout after 30 seconds",
            "Step timeout error"
        ]
    }
}