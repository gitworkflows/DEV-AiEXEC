"""Aiexec backwards compatibility layer.

This module provides backwards compatibility by forwarding imports from
aiexec.* to lfx.* to maintain compatibility with existing code that
references the old aiexec module structure.
"""

import importlib
import importlib.util
import sys
from types import ModuleType
from typing import Any


class AiexecCompatibilityModule(ModuleType):
    """A module that forwards attribute access to the corresponding lfx module."""

    def __init__(self, name: str, lfx_module_name: str):
        super().__init__(name)
        self._lfx_module_name = lfx_module_name
        self._lfx_module = None

    def _get_lfx_module(self):
        """Lazily import and cache the lfx module."""
        if self._lfx_module is None:
            try:
                self._lfx_module = importlib.import_module(self._lfx_module_name)
            except ImportError as e:
                msg = f"Cannot import {self._lfx_module_name} for backwards compatibility with {self.__name__}"
                raise ImportError(msg) from e
        return self._lfx_module

    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the lfx module with caching."""
        lfx_module = self._get_lfx_module()
        try:
            attr = getattr(lfx_module, name)
        except AttributeError as e:
            msg = f"module '{self.__name__}' has no attribute '{name}'"
            raise AttributeError(msg) from e
        else:
            # Cache the attribute in our __dict__ for faster subsequent access
            setattr(self, name, attr)
            return attr

    def __dir__(self):
        """Return directory of the lfx module."""
        try:
            lfx_module = self._get_lfx_module()
            return dir(lfx_module)
        except ImportError:
            return []


def _setup_compatibility_modules():
    """Set up comprehensive compatibility modules for aiexec.base imports."""
    # First, set up the base attribute on this module (aiexec)
    current_module = sys.modules[__name__]

    # Define all the modules we need to support
    module_mappings = {
        # Core base module
        "aiexec.base": "lfx.base",
        # Inputs module - critical for class identity
        "aiexec.inputs": "lfx.inputs",
        "aiexec.inputs.inputs": "lfx.inputs.inputs",
        # Schema modules - also critical for class identity
        "aiexec.schema": "lfx.schema",
        "aiexec.schema.data": "lfx.schema.data",
        "aiexec.schema.serialize": "lfx.schema.serialize",
        # Template modules
        "aiexec.template": "lfx.template",
        "aiexec.template.field": "lfx.template.field",
        "aiexec.template.field.base": "lfx.template.field.base",
        # Components modules
        "aiexec.components": "lfx.components",
        "aiexec.components.helpers": "lfx.components.helpers",
        "aiexec.components.helpers.calculator_core": "lfx.components.helpers.calculator_core",
        "aiexec.components.helpers.create_list": "lfx.components.helpers.create_list",
        "aiexec.components.helpers.current_date": "lfx.components.helpers.current_date",
        "aiexec.components.helpers.id_generator": "lfx.components.helpers.id_generator",
        "aiexec.components.helpers.memory": "lfx.components.helpers.memory",
        "aiexec.components.helpers.output_parser": "lfx.components.helpers.output_parser",
        "aiexec.components.helpers.store_message": "lfx.components.helpers.store_message",
        # Individual modules that exist in lfx
        "aiexec.base.agents": "lfx.base.agents",
        "aiexec.base.chains": "lfx.base.chains",
        "aiexec.base.data": "lfx.base.data",
        "aiexec.base.data.utils": "lfx.base.data.utils",
        "aiexec.base.document_transformers": "lfx.base.document_transformers",
        "aiexec.base.embeddings": "lfx.base.embeddings",
        "aiexec.base.flow_processing": "lfx.base.flow_processing",
        "aiexec.base.io": "lfx.base.io",
        "aiexec.base.io.chat": "lfx.base.io.chat",
        "aiexec.base.io.text": "lfx.base.io.text",
        "aiexec.base.langchain_utilities": "lfx.base.langchain_utilities",
        "aiexec.base.memory": "lfx.base.memory",
        "aiexec.base.models": "lfx.base.models",
        "aiexec.base.models.google_generative_ai_constants": "lfx.base.models.google_generative_ai_constants",
        "aiexec.base.models.openai_constants": "lfx.base.models.openai_constants",
        "aiexec.base.models.anthropic_constants": "lfx.base.models.anthropic_constants",
        "aiexec.base.models.aiml_constants": "lfx.base.models.aiml_constants",
        "aiexec.base.models.aws_constants": "lfx.base.models.aws_constants",
        "aiexec.base.models.groq_constants": "lfx.base.models.groq_constants",
        "aiexec.base.models.novita_constants": "lfx.base.models.novita_constants",
        "aiexec.base.models.ollama_constants": "lfx.base.models.ollama_constants",
        "aiexec.base.models.sambanova_constants": "lfx.base.models.sambanova_constants",
        "aiexec.base.prompts": "lfx.base.prompts",
        "aiexec.base.prompts.api_utils": "lfx.base.prompts.api_utils",
        "aiexec.base.prompts.utils": "lfx.base.prompts.utils",
        "aiexec.base.textsplitters": "lfx.base.textsplitters",
        "aiexec.base.tools": "lfx.base.tools",
        "aiexec.base.vectorstores": "lfx.base.vectorstores",
    }

    # Create compatibility modules for each mapping
    for aiexec_name, lfx_name in module_mappings.items():
        if aiexec_name not in sys.modules:
            # Check if the lfx module exists
            try:
                spec = importlib.util.find_spec(lfx_name)
                if spec is not None:
                    # Create compatibility module
                    compat_module = AiexecCompatibilityModule(aiexec_name, lfx_name)
                    sys.modules[aiexec_name] = compat_module

                    # Set up the module hierarchy
                    parts = aiexec_name.split(".")
                    if len(parts) > 1:
                        parent_name = ".".join(parts[:-1])
                        parent_module = sys.modules.get(parent_name)
                        if parent_module is not None:
                            setattr(parent_module, parts[-1], compat_module)

                    # Special handling for top-level modules
                    if aiexec_name == "aiexec.base":
                        current_module.base = compat_module
                    elif aiexec_name == "aiexec.inputs":
                        current_module.inputs = compat_module
                    elif aiexec_name == "aiexec.schema":
                        current_module.schema = compat_module
                    elif aiexec_name == "aiexec.template":
                        current_module.template = compat_module
                    elif aiexec_name == "aiexec.components":
                        current_module.components = compat_module
            except (ImportError, ValueError):
                # Skip modules that don't exist in lfx
                continue

    # Handle modules that exist only in aiexec (like knowledge_bases)
    # These need special handling because they're not in lfx yet
    aiexec_only_modules = {
        "aiexec.base.data.kb_utils": "aiexec.base.data.kb_utils",
        "aiexec.base.knowledge_bases": "aiexec.base.knowledge_bases",
        "aiexec.components.knowledge_bases": "aiexec.components.knowledge_bases",
    }

    for aiexec_name in aiexec_only_modules:
        if aiexec_name not in sys.modules:
            try:
                # Try to find the actual physical module file
                from pathlib import Path

                base_dir = Path(__file__).parent

                if aiexec_name == "aiexec.base.data.kb_utils":
                    kb_utils_file = base_dir / "base" / "data" / "kb_utils.py"
                    if kb_utils_file.exists():
                        spec = importlib.util.spec_from_file_location(aiexec_name, kb_utils_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[aiexec_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("aiexec.base.data")
                            if parent_module is not None:
                                parent_module.kb_utils = module

                elif aiexec_name == "aiexec.base.knowledge_bases":
                    kb_dir = base_dir / "base" / "knowledge_bases"
                    kb_init_file = kb_dir / "__init__.py"
                    if kb_init_file.exists():
                        spec = importlib.util.spec_from_file_location(aiexec_name, kb_init_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[aiexec_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("aiexec.base")
                            if parent_module is not None:
                                parent_module.knowledge_bases = module

                elif aiexec_name == "aiexec.components.knowledge_bases":
                    components_kb_dir = base_dir / "components" / "knowledge_bases"
                    components_kb_init_file = components_kb_dir / "__init__.py"
                    if components_kb_init_file.exists():
                        spec = importlib.util.spec_from_file_location(aiexec_name, components_kb_init_file)
                        if spec is not None and spec.loader is not None:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[aiexec_name] = module
                            spec.loader.exec_module(module)

                            # Also add to parent module
                            parent_module = sys.modules.get("aiexec.components")
                            if parent_module is not None:
                                parent_module.knowledge_bases = module
            except (ImportError, AttributeError):
                # If direct file loading fails, skip silently
                continue


# Set up all the compatibility modules
_setup_compatibility_modules()
