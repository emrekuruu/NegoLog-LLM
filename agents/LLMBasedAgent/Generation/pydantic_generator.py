from typing import Dict, Any, Annotated
from pydantic import BaseModel, Field, create_model
from enum import Enum

def create_issue_enum(issue_dict: Dict[str, float], enum_name: str) -> type[Enum]:
    """Creates an Enum class from a dictionary of issue values."""
    return Enum(enum_name, {k: k for k in issue_dict.keys()})

def generate_pydantic_class(issues_dict: Dict[str, Dict[str, float]], class_name: str = "OfferSchema") -> type[BaseModel]:
    """
    Generates a Pydantic class from a dictionary of issues.
    
    Args:
        issues_dict: Dictionary containing issue categories and their possible values
        class_name: Name of the generated Pydantic class
    
    Returns:
        A Pydantic class with attributes for each issue category
    """
    field_definitions = {}
    
    for issue_name, values in issues_dict.items():
        enum_class = create_issue_enum(values, f"{issue_name}Enum")
        field_name = str(issue_name)
        field_definitions[field_name] = (
            enum_class | None,  # Type annotation
            Field(
                default=None,
                description=f"Must be one of: {', '.join(values.keys())}"
            )
        )

    field_definitions["reasoning"] = (str | None, Field(default=None))

    return create_model(class_name, **field_definitions)

