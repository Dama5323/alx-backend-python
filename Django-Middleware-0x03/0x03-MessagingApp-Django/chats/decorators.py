def role_required(*roles):
    """
    Decorator for views that checks whether a user has a particular role enabled.
    """
    def decorator(view_func):
        view_func.role_required = roles
        return view_func
    return decorator