"""Custom Sphinx extension to add multiple JupyterHub launch buttons."""

from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode

from docutils.nodes import document
from sphinx.application import Sphinx
from sphinx_book_theme.header_buttons import get_repo_url, get_repo_parts


def add_multiple_jupyterhub_buttons(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: Optional[document],
):
    """Add multiple JupyterHub launch buttons to the page context.
    
    This function runs after the standard launch buttons are added and appends
    additional JupyterHub buttons based on the 'jupyterhub_servers' configuration.
    """
    config_theme = app.config["html_theme_options"]
    launch_buttons = config_theme.get("launch_buttons", {})
    jupyterhub_servers = launch_buttons.get("jupyterhub_servers", [])
    
    # If there are no additional servers configured, do nothing
    if not jupyterhub_servers:
        return
    
    # Check if this page should have launch buttons (must be a notebook)
    if "header_buttons" not in context:
        return
    
    header_buttons = context.get("header_buttons", [])
    
    # Find the existing launch buttons list
    launch_buttons_list = None
    for button in header_buttons:
        if isinstance(button, dict) and button.get("type") in ("dropdown", "group"):
            if button.get("tooltip") and "Launch" in button.get("tooltip", ""):
                launch_buttons_list = button.get("buttons", [])
                break
    
    # If we don't have a launch buttons dropdown yet, check if there's a direct button list
    if launch_buttons_list is None:
        # Look for launch_buttons in context
        if "launch_buttons" in context:
            launch_buttons_list = context["launch_buttons"]
    
    if launch_buttons_list is None:
        return
    
    # Get repository information using the same functions as the original launch buttons
    repo_url, _ = get_repo_url(context)
    provider_url, org, repo, provider = get_repo_parts(context)
    
    if org is None and repo is None:
        return
    
    # Get the branch from config
    branch = config_theme.get("repository", {}).get("branch", "main")
    
    # Get the notebook interface preference
    notebook_interface = launch_buttons.get("notebook_interface", "classic")
    notebook_interface_prefixes = {"classic": "tree", "jupyterlab": "lab/tree"}
    ui_pre = notebook_interface_prefixes.get(notebook_interface, "tree")
    
    # Get the path to the current file
    book_relpath = config_theme.get("path_to_docs", "").strip("/")
    if book_relpath != "":
        book_relpath += "/"
    
    path = app.env.doc2path(pagename)
    extension = Path(path).suffix
    
    # Check if we have a non-ipynb file, but an ipynb of same name exists
    if extension != ".ipynb" and Path(path).with_suffix(".ipynb").exists():
        extension = ".ipynb"
    
    path_rel_repo = f"{book_relpath}{pagename}{extension}"
    
    # Remove the default JupyterHub button if it exists
    original_jupyterhub_idx = None
    for idx, button in enumerate(launch_buttons_list):
        if isinstance(button, dict) and button.get("text") == "JupyterHub":
            original_jupyterhub_idx = idx
            break
    
    # Remove the original button if we found it
    if original_jupyterhub_idx is not None:
        launch_buttons_list.pop(original_jupyterhub_idx)
    
    # Add each JupyterHub server as a button
    for server in jupyterhub_servers:
        server_url = server.get("url", "").strip("/")
        server_text = server.get("text", "JupyterHub")
        
        if not server_url:
            continue
        
        url_params = urlencode(
            dict(
                repo=repo_url,
                urlpath=f"{ui_pre}/{repo}/{path_rel_repo}",
                branch=branch
            ),
            safe="/",
        )
        url = f"{server_url}/hub/user-redirect/git-pull?{url_params}"
        
        launch_buttons_list.append(
            {
                "type": "link",
                "text": server_text,
                "tooltip": f"Launch on {server_text}",
                "icon": "_static/images/logo_jupyterhub.svg",
                "url": url,
            }
        )


def setup(app: Sphinx):
    """Setup the Sphinx extension."""
    # Connect to the html-page-context event with high priority to run after
    # the default launch buttons are added
    app.connect("html-page-context", add_multiple_jupyterhub_buttons, priority=1000)
    
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
