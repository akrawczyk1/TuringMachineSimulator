# Turing Machine Simulator — Project Roadmap

## Phase 1 — Finish the Core Simulator
- [x] Complete and harden `step()` — bounds checking, missing transition handling, halt-before-step guard
- [ ] Write `run()` — loops `step()` until halt or step limit
- [ ] Write pytest tests for `step()` and `run()`

## Phase 2 — Backend API
- [ ] Endpoint to run a machine to completion
- [ ] Endpoint to advance one step at a time
- [ ] Endpoint to load a machine from a JSON file
- [ ] Endpoint to export machine state as JSON

## Phase 3 — React Frontend (Static)
- [ ] Project setup
- [ ] File upload / download UI
- [ ] Tape visualization component
- [ ] Transition table configuration UI

## Phase 4 — Integration
- [ ] Wire frontend to backend over HTTP
- [ ] Step-through animation with speed control

## Phase 5 — Packaging
- [ ] pywebview integration
- [ ] PyInstaller bundling

## Phase 6 — Stretch Goal: Rust Simulator Core
- [ ] Rewrite `step()` and `run()` in Rust
- [ ] Expose Rust implementation to Python via PyO3 + Maturin
- [ ] Validate correctness against existing Python implementation
- [ ] Headless / terminal-based interface for compute-heavy workloads
