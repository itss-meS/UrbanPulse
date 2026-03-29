# UrbanPulse

<div align="center">

![UrbanPulse Banner](imgs/Screenshot%202026-03-29%20110537.png)

*Transforming urban motion into living visual poetry*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TouchDesigner](https://img.shields.io/badge/TouchDesigner-v2.1-blue)](https://derivative.ca/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)

</div>

---

## 🌆 Overview

**UrbanPulse** is a real-time generative art project that transforms raw video footage of urban environments into mesmerizing visual experiences. Built with TouchDesigner and NumPy, it detects motion and edges in video streams and converts them into three distinct artistic styles—from typographic expression to colorful geometric networks.

This project wasn't for a grade or a client—it was built purely for the fun of the process and the satisfaction of seeing raw video data turn into a living, breathing visualization.

## ✨ Features

### Three Unique Visualization Modes

1. **Typographic Motion Trails** (`script1.py`)
   - Traces motion with flowing text
   - Customizable message: "CALX WRITES THE MOTION"
   - Persistent fade effect creates ghostly trails
   - Adjustable parameters for speed, scale, and jitter

2. **Multi-Letter Edge Burst** (`script2.py`)
   - Spawns letters in cardinal directions from edge points
   - Creates explosive, dynamic compositions
   - Random character selection for organic variety

3. **Chromatic Line Networks** (`script3.py`)
   - Connects motion points with vibrant colored lines
   - Builds evolving geometric patterns
   - Frame-to-frame point tracking creates flowing networks

### Technical Highlights

- **Real-time Processing**: Processes video feeds at interactive framerates
- **Edge Detection**: Custom threshold-based edge detection algorithm
- **Pixel-Perfect Rendering**: 5×7 bitmap font rendering for crisp typography
- **Persistent Canvas**: Fade effects create motion history visualization
- **Adaptive Sampling**: Intelligent point selection prevents performance bottlenecks

## 🎨 Gallery

<table>
  <tr>
    <td><img src="imgs/Screenshot%202026-03-29%20110355.png" alt="Night City Scene" /></td>
    <td><img src="imgs/Screenshot%202026-03-29%20110537.png" alt="Park Scene" /></td>
  </tr>
  <tr>
    <td align="center"><em>Urban nightscape with chromatic networks</em></td>
    <td align="center"><em>Daytime park activity visualization</em></td>
  </tr>
</table>

## 🚀 Quick Start

### Prerequisites

- **TouchDesigner** (v2.1 or higher) - [Download here](https://derivative.ca/)
- **Python 3.8+** with NumPy
- A video source (webcam, video file, or live feed)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/UrbanPulse.git
   cd UrbanPulse
   ```

2. **Open the TouchDesigner project**
   ```bash
   # Open the .toe file in TouchDesigner
   TouchDesigner/Cool_V2.1.toe
   ```

3. **Load your visualization script**
   - In TouchDesigner, locate the Script TOP node
   - Choose one of the three scripts (`script1.py`, `script2.py`, or `script3.py`)
   - Connect your video input

4. **Adjust and play!**
   - Tweak parameters in real-time
   - Experiment with different video sources
   - Export your results

## ⚙️ Configuration

### Script 1: Typographic Trails

```python
THRESH = 0.5      # Edge detection sensitivity (0.0-1.0)
RATE = 60         # Letters spawned per frame
SCALE = 1         # Letter size multiplier
FADE = 0.90       # Canvas persistence (0.0-1.0)
JITTER = 2.0      # Position randomness
TEXT = "CALX WRITES THE MOTION "  # Your custom message
```

### Script 2: Edge Burst

```python
# Spawns 60 random letters per frame
# Cardinal offsets: [8,0], [-8,0], [0,8], [0,-8]
# Automatic random letter selection from full alphabet
```

### Script 3: Chromatic Networks

```python
THRESH = 0.5      # Edge detection threshold
POINTS = 80       # Points tracked per frame
FADE = 0.5        # Trail persistence
JITTER = 1.0      # Line endpoint randomness
```

## 📊 Technical Deep Dive

### Edge Detection Algorithm

All three scripts use a custom threshold-based edge detector:

```python
def edges_from_thresh(gray, threshold):
    """
    Detects edges by finding pixels where neighboring 
    pixels cross the threshold boundary.
    """
    mask = (gray >= threshold).astype(np.uint8)
    
    # Check all 4 cardinal directions
    up    = np.roll(mask, -1, 0)
    down  = np.roll(mask,  1, 0)
    left  = np.roll(mask,  1, 1)
    right = np.roll(mask, -1, 1)
    
    # Edge where any neighbor differs
    edge = mask & ((up != mask) | (down != mask) | 
                   (left != mask) | (right != mask))
    
    return edge
```

### Rendering Pipeline

1. **Input Processing**: RGBA video → Grayscale conversion
2. **Feature Extraction**: Edge detection on grayscale
3. **Point Sampling**: Intelligent selection of edge points
4. **Visualization**: Draw letters/lines at selected points
5. **Canvas Update**: Apply fade effect and output

## 🎯 Use Cases

- **Live VJ Performances**: Real-time visuals for music events
- **Art Installations**: Interactive public displays
- **Video Processing**: Create unique effects for film/video
- **Data Visualization**: Represent motion patterns in urban studies
- **Creative Coding Education**: Learn real-time graphics programming

## 🛠️ Project Structure

```
UrbanPulse/
├── TouchDesigner/
│   └── Cool_V2.1.toe          # Main TouchDesigner project
├── imgs/
│   ├── Screenshot...png        # Sample outputs
│   └── Screen Recording...mp4  # Demo video
├── script1.py                  # Typographic motion trails
├── script2.py                  # Multi-letter edge burst
├── script3.py                  # Chromatic line networks
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## 🧪 Experimentation Ideas

- **Custom Typography**: Add your own bitmap fonts or import vector fonts
- **Color Palettes**: Replace white with gradients or themed color schemes
- **Audio Reactivity**: Make parameters respond to music or sound levels
- **3D Projection**: Map outputs onto 3D geometry in TouchDesigner
- **Machine Learning**: Combine with pose estimation or object detection
- **Multi-camera**: Blend visualizations from multiple video sources

## 🎓 Learning Resources

If you're new to TouchDesigner or generative art:

- [TouchDesigner Documentation](https://docs.derivative.ca/)
- [NumPy for Image Processing](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Creative Coding Community](https://derivative.ca/community)

## 🤝 Contributing

This is a personal art project, but contributions and experiments are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-viz`)
3. Commit your changes (`git commit -m 'Add amazing visualization'`)
4. Push to the branch (`git push origin feature/amazing-viz`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2026 SHREY GALGALE**

## 🙏 Acknowledgments

- Built with love using **TouchDesigner** by Derivative
- Inspired by urban landscapes and the poetry of motion
- Thanks to the creative coding community for endless inspiration

## 📫 Connect

Have questions or want to share your own experiments?

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/UrbanPulse/issues)
- **Discussions**: Share your creations and ideas

---

<div align="center">

**Made with ❤️ and lots of pixels**

*UrbanPulse transforms the chaos of city life into visual harmony*

</div>
