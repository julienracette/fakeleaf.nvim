# fakeleaf.nvim

## 📌 Overview

`fakeleaf.nvim` is an experimental Neovim plugin that aims to bring Overleaf projects directly into Neovim.

The goal is to allow users to:

* Open and edit Overleaf LaTeX projects locally
* Synchronize changes between Neovim and Overleaf
* Eventually support real-time collaboration using Operational Transform (OT)

This plugin acts as the **frontend layer**, handling buffers, UI, and user interaction inside Neovim.

---

## 🧠 Architecture

```
Neovim (fakeleaf.nvim)
        ↓
Python backend (fakeleaf-bridge)
        ↓
Overleaf WebSocket (OT)
```

* Lua handles editor integration
* Python handles networking and synchronization

---

## 🚧 Current Status

⚠️ **Early-stage experimental project**

* Not stable
* APIs and structure may change
* Many features are incomplete or under development

---

## 🧪 Local Development Disclaimer

This repository currently contains:

* Hardcoded paths
* Machine-specific configurations
* Debug and test code

👉 These are **specific to my local environment** and are **not ready for general use**.

You will likely need to adapt paths and configuration manually.

---

## ⚖️ Disclaimer

* This project is **not affiliated with Overleaf**
* It is intended for **educational and experimental purposes only**
* It does **not aim to interfere with or abuse Overleaf services**

If the Overleaf team has any concerns, they are welcome to **contact me personally**, and I will address them promptly.

---

## 📦 Installation

Using lazy.nvim:

```lua
{
  "julienracette/fakeleaf.nvim",
}
```

⚠️ The plugin depends on the Python backend (`fakeleaf-bridge`).

---

## 🔗 Related Project

Backend:

* https://github.com/julienracette/fakeleaf-bridge

---

## 🔮 Future Plans

* Clean configuration system
* Removal of hardcoded paths
* Stable synchronization layer
* Real-time collaboration support
* Improved installation process

---

## 🤝 Contributions

Contributions are welcome, but expect rapid changes and breaking updates.

---

## 📄 License

MIT License
