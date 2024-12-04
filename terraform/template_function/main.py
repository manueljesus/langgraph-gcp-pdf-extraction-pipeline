import functions_framework

@functions_framework.cloud_event
def hello_world(cloud_event):
    """Cloud Event Function.

    Args:
        cloud_event: The Cloud Event that triggered the function.
    """
    print("Hello, World!")
