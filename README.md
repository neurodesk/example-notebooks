# example-notebooks

#### Table of Contents
**[Getting Started](#getting-started)**<br>
**[Design Principles](#design-principles)**<br>
**[Tips](#tips)**<br>

If you're planning to create a new example notebook, please follow these steps:

## Getting Started
1. **Access the Template**: Start by accessing the `template.ipynb` file. This is our standard template for creating new example notebooks which includes the standard metadata requirements, `watermark` for dependency tracking, and `module load` commands for neuroimaging software, and a table of contents example for structuring longer notebooks.
2. **Create a New Notebook**: Make sure your notebook runs as expected. An automatic GitHub Action will block the publication of your Example Notebook if it does not run entirely.
3. **Save and Submit**: Once you're done, save your notebook and submit it for review by creating a pull request on our GitHub repository.

## Design Principles

Our example notebooks follow best practices from [Rule et al. (2019) "Ten simple rules for writing and sharing computational analyses in Jupyter Notebooks"](https://doi.org/10.1371/journal.pcbi.1007007). Below are the key principles adapted for the Neurodesk platform:

### 1. Tell a Story for Your Audience
- Interleave explanatory markdown with code and results to create an interactive tutorial
- Identify your target audience early (e.g., clinical researchers, students, those new to neuroimaging)
- Don't assume prior knowledge: over-explanation is better than under-explanation

### 2. Document Your Process and Reasoning
- Document not just what you did, but *why* you made specific choices
- Explain parameter selections and decision points in your analysis
- Include your reasoning and intuition alongside reproducible code

### 3. Use Clear Cell and Notebook Structure
- Keep each cell focused on one meaningful analysis step
- Avoid long cells (>100 lines of code)
- Use descriptive markdown headers to organize your notebook into clear sections
- Consider splitting very long analyses into a series of connected notebooks
- Use markdown to create a table of contents for longer notebooks
- For cells with lengthy output, add the `scroll-output` tag via Property Inspector to enable scrolling

### 4. Modularise Your Code
- Create reusable helper functions for repetitive tasks; this makes your notebook more modular and helps users adapt your code to their own data

### 5. Build a Reproducible Pipeline
- Declare key variables and parameters at the beginning of your notebook
- Perform all preparatory steps (like data cleaning) within the notebook—avoid manual interventions
- Before submitting, restart the kernel and run all cells to ensure full reproducibility

### 6. Use Open, Well-Documented Data
- Base your examples on openly available datasets and cite them at the beginning of your notebook with DOIs or permanent links (see template for format)
- Document all data preprocessing steps and explain any derived dataset transformations

### 7. Design for READ, RUN, and EXPLORE

**We provide for you:**
- Version control via GitHub with automated testing via GitHub Actions
- Zero-install testing environment via Neurodesk Play
- Template with `watermark` and `module load` for dependency management
- Static rendering on GitHub Pages

**When creating your notebook:**
- **READ**: Write clear explanations so users can understand your analysis without running it
- **RUN**: Your notebook executes completely from top to bottom without errors (GitHub Actions will verify this, but test locally first to save time)
- **EXPLORE**: Structure your code so users can easily modify parameters, use their own data, or extract specific sections for reuse

### 8. Advocate for Open, Reproducible Research
- Before submitting, ask a colleague to run your notebook and note any difficulties
- Consider how users might adapt your notebook for their own research questions
- Think of your notebook as both a tutorial and a template for others

## Tips

### Managing Long Outputs

**For cells that produce long outputs** (e.g., extensive logs, large dataframes, verbose model training), add the `scroll-output` tag to make the output scrollable when rendered on GitHub Pages.

**How to add:**
1. Select the cell with long output
2. Open the Property Inspector (right or left sidebar, or View → Show Property Inspector)
3. Under "Common Tools" → "Cell Tags", add Tag: `scroll-output`

This prevents long outputs from dominating the page layout.
