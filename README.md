# HER Hack-Astron #7 | Spark-X2.6 Open Source AI for Good Challenge

## Event Overview
- **Issue Link**: [GitHub Issue #16](https://github.com/XHToken/Spark-X2.6/issues/16)
- **Model**: [XHToken/Spark-X2.6-4B on Hugging Face](https://huggingface.co/XHToken/Spark-X2.6-4B) (Revision sha: `d1b5f26071101c27fcd07728e7a7770e428281f4`)
- **Community Discussions Submission**: [Spark-X2.6-4B Discussions](https://huggingface.co/XHToken/Spark-X2.6-4B/discussions)
- **Deadline**: October 31, 2026, 23:59 UTC (November 1, 2026, 07:59 UTC+8)
- **Prize**: USD 100 for 1 winner (Champion title)

## Requirements & Submission Rules
1. **Participation**: Individuals or teams. If team, >= 50% must identify as women.
2. **Model usage**: Must genuinely use `Spark-X2.6-4B` and explain its specific role.
3. **Demo**: Video demo (2-5 mins) OR illustrated demo (step-by-step screenshots with inputs/outputs).
4. **Publishing Steps**:
   - Give the model a ❤️ Like on Hugging Face.
   - Post project in [Hugging Face Community Discussions](https://huggingface.co/XHToken/Spark-X2.6-4B/discussions) with title formatted as `[HER Hack-Astron # 7] [Track] <Project Name>`.
   - Reply to [GitHub Issue #16](https://github.com/XHToken/Spark-X2.6/issues/16) with your Hugging Face discussion link.

## Tracks
- Disaster preparedness and response
- Health and well-being
- Accessibility (e.g. simplifying complex text, plain-language translation)
- Gender equality
- Other public interest (elderly support, education, mutual aid)

## System & Execution Environment
- **Host Specs**: Windows, Intel HD Graphics 520 (integrated GPU), 8GB RAM, ~16GB free disk.
- **Inference Strategy**:
  - The raw BF16 model is ~8-12 GB, which will strain 8 GB RAM.
  - Recommended for fast execution on this machine: GGUF quantized version (`Q4_K_M` ~2.5GB or `VladHong/Spark-X2.6-4B-2GB-GGUF`) via `llama-cpp-python` or lightweight Web/Transformers CPU execution, or hosting an endpoint/WebGPU space.
