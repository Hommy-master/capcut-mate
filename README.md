# CapCut Mate API

### 🌐 Language Switch
[中文版](README.zh.md) | [English](README.md)

## Project Introduction
CapCut Mate API is a Jianying draft automation assistant built on FastAPI, providing rich API interfaces to create and edit Jianying drafts. It supports creating drafts, adding materials such as videos/audio/images/subtitles/effects, saving drafts, and cloud rendering. It can be deployed as a Coze plugin with one-click setup.

## Project Resources
- [Jianying Assistant](https://github.com/Hommy-master/capcut-mate)
- [Jianying Assistant - Coze Plugin](https://www.coze.cn/store/plugin/7576197869707722771)

⭐ If you find this project helpful, please give us a Star! Your support is the greatest motivation for me to continuously maintain and improve the project 😊

## Features
- 🎬 Draft Management: Create draft, get draft, save draft
- 🎥 Material Addition: Add videos, audios, images, stickers, subtitles, effects, masks, etc.
- 🔧 Advanced Functions: Keyframe control, text styles, animation effects, etc.
- 📤 Video Export: Cloud rendering to generate final video
- 🛡️ Data Validation: Using Pydantic for request data validation
- 📖 RESTful API: Compliant with standard API design specifications
- 📚 Auto Documentation: FastAPI automatically generates interactive API documentation

## Tech Stack
- Python 3.11+
- FastAPI: High-performance web framework
- Pydantic: Data validation and model definition
- Passlib: Password encryption (if using user authentication)
- Uvicorn: ASGI server
- uv: Python package manager and project management tool

## Quick Start

### Prerequisites
- Python 3.11+
- uv: Python package manager and project management tool

Installation:
#### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Linux/macOS
```bash
sh -c "$(curl -LsSf https://astral.sh/uv/install.sh)"
```

### Installation Steps
1. Clone the project
```bash
git clone git@github.com:Hommy-master/capcut-mate.git
cd capcut-mate
```

2. Install dependencies
```bash
# Install dependencies
uv sync

# Additional execution for Windows
uv pip install -e .[windows]
```

3. Start the server
```bash
uv run main.py
```

4. Access API documentation
After starting, visit http://localhost:30000/docs to view the automatically generated interactive API documentation

### Container Deployment
```bash
docker pull gogoshine/capcut-mate:latest
docker run -p 30000:30000 gogoshine/capcut-mate:latest
```

Or use docker-compose:
```bash
docker-compose up -d
```

## One-Click Import Coze Plugin

1. Open Coze platform: https://coze.cn/home

   ![Step 1](./assets/coze1.png)

2. Add Plugin

   ![Step 2](./assets/coze2.png)

3. Import Plugin

   ![Step 3](./assets/coze3.png)

4. Upload the openapi.yaml file in the current project directory

   ![Step 4](./assets/coze4.png)

5. Complete file upload

   ![Step 5](./assets/coze5.png)

6. Complete logo replacement

   ![Step 6](./assets/coze6.png)

7. Enable Plugin

   ![Step 7](./assets/coze7.png)

## API Documentation

The following are the core interfaces provided by CapCut Mate API, supporting a complete video creation workflow:

### 🏗️ Draft Management
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **create_draft** | Create Draft | Create a new Jianying draft project, set canvas size | [📖 View Documentation](./docs/create_draft.md) |
| **save_draft** | Save Draft | Save current draft state, ensure edit content persistence | [📖 View Documentation](./docs/save_draft.md) |
| **get_draft** | Get Draft | Get draft file list and detailed information | [📖 View Documentation](./docs/get_draft.md) |

### 🎥 Video Materials
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **add_videos** | Add Videos | Batch add video materials, support cropping, scaling, effects | [📖 View Documentation](./docs/add_videos.md) |
| **add_images** | Add Images | Batch add image materials, support animations and transition effects | [📖 View Documentation](./docs/add_images.md) |
| **add_sticker** | Add Stickers | Add decorative stickers, support position and size adjustment | [📖 View Documentation](./docs/add_sticker.md) |

### 🎵 Audio Processing
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **add_audios** | Add Audios | Batch add audio materials, support volume and fade in/out | [📖 View Documentation](./docs/add_audios.md) |
| **get_audio_duration** | Get Audio Duration | Get precise duration information of audio files | [📖 View Documentation](./docs/get_audio_duration.md) |

### 📝 Text Subtitles
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **add_captions** | Add Captions | Batch add captions, support keyword highlighting and style settings | [📖 View Documentation](./docs/add_captions.md) |
| **add_text_style** | Text Style | Create rich text styles, support keyword colors and fonts | [📖 View Documentation](./docs/add_text_style.md) |

### ✨ Effects & Animations
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **add_effects** | Add Effects | Add visual effects, such as filters, borders, dynamic effects | [📖 View Documentation](./docs/add_effects.md) |
| **add_keyframes** | Keyframe Animation | Create property animations for position, scale, rotation, etc. | [📖 View Documentation](./docs/add_keyframes.md) |
| **add_masks** | Mask Effects | Add various shape masks, control visible areas of the screen | [📖 View Documentation](./docs/add_masks.md) |

### 🎨 Animation Resources
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **get_text_animations** | Text Animations | Get available text entrance, exit, and loop animations | [📖 View Documentation](./docs/get_text_animations.md) |
| **get_image_animations** | Image Animations | Get available image animation effects list | [📖 View Documentation](./docs/get_image_animations.md) |

### 🎬 Video Generation
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **gen_video** | Generate Video | Submit video rendering task, asynchronous processing | [📖 View Documentation](./docs/gen_video.md) |
| **gen_video_status** | Query Status | Query the progress and status of video generation tasks | [📖 View Documentation](./docs/gen_video_status.md) |

### 🚀 Quick Tools
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **easy_create_material** | Quick Creation | Add multiple types of materials at once, simplify creation process | [📖 View Documentation](./docs/easy_create_material.md) |

###🛠️ Utility Tools
| Interface | Function | Description | Documentation Link |
|-----------|----------|-------------|-------------------|
| **get_url** | Extract URL | Extract URL information from input content | [📖 View Documentation](./docs/get_url.md) |
| **search_sticker** | Search Sticker | Search sticker materials by keyword | [📖 View Documentation](./docs/search_sticker.md) |
| **objs_to_str_list** | Objects to String List | Convert object list to string list format | [📖 View Documentation](./docs/objs_to_str_list.md) |
| **str_list_to_objs** | String List to Objects | Convert string list to object list format | [📖 View Documentation](./docs/str_list_to_objs.md) |
| **str_to_list** | String to List | Convert string to list format | [📖 View Documentation](./docs/str_to_list.md) |
| **timelines** | Create Timelines | Generate timeline configurations for video editing | [📖 View Documentation](./docs/timelines.md) |
| **audio_timelines** | Audio Timelines | Calculate timelines based on audio durations | [📖 View Documentation](./docs/audio_timelines.md) |
| **audio_infos** | Audio Information | Generate audio information from URLs and timelines | [📖 View Documentation](./docs/audio_infos.md) |
| **imgs_infos** | Image Information | Generate image information from URLs and timelines | [📖 View Documentation](./docs/imgs_infos.md) |
| **caption_infos** | Caption Information | Generate caption information from text and timelines | [📖 View Documentation](./docs/caption_infos.md) |
| **effect_infos** | Effect Information | Generate effect information from names and timelines | [📖 View Documentation](./docs/effect_infos.md) |
| **keyframes_infos** | Keyframe Information | Generate keyframe information from configurations | [📖 View Documentation](./docs/keyframes_infos.md) |
| **video_infos** | Video Information | Generate video information from URLs and timelines | [📖 View Documentation](./docs/video_infos.md) |

## API Usage Examples

### Create Draft
```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/create_draft" \
-H "Content-Type: application/json" \
-d '{"width": 1080, "height": 1920}'
```

### Add Videos
```bash
curl -X POST "http://localhost:30000/openapi/capcut-mate/v1/add_videos" \
-H "Content-Type: application/json" \
-d '{
  "draft_url": "http://localhost:30000/openapi/capcut-mate/v1/get_draft?draft_id=20251126212753cab03392",
  "video_infos": [
    {
      "url": "https://example.com/video.mp4",
      "start": 0,
      "end": 1000000
    }
  ]
}'
```

## API Documentation
- Local Access: http://localhost:30000/docs
- ReDoc Version: http://localhost:30000/redoc

## Jianying Assistant Client

The Jianying Assistant client provides a convenient desktop interface. Here are the startup methods:

### macOS Sandbox Permissions Guide

When running on macOS, the application may request access permissions for specific folders. Please follow these steps:

1. If permission prompts appear during the first run, allow the application to access the required folders
2. For manual configuration, go to `System Preferences > Security & Privacy > Privacy > Folder Access`
3. Ensure the CapCut Mate application is added to the allowed list

For more details, please refer to the [macOS Sandbox Permissions Configuration Guide](./docs/macos_sandbox_setup.md).

1. Install Dependencies

```bash
# Switch npm mirror source - for Windows
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/

# Switch yarn mirror source - for Linux or macOS
export ELECTRON_MIRROR="https://npmmirror.com/mirrors/electron/"

# Install dependencies
npm install --verbose
```

2. Start the Project

```bash
npm run web:dev
npm start
```

## Open Source Community Discussion Group
- WeChat Group:

  <img src="./assets/wechat-q.jpg" width="344" height="498" alt="Jianying Assistant">

## Business Cooperation
- WeChat:

  <img src="./assets/wechat.jpg" width="220" height="220" alt="Technical Support WeChat">

- Email: taohongmin51@gmail.com

---