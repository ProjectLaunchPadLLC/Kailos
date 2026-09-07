# Kailos Computational Fabric
## Foundational Design

**Organization:** ProjectLaunchPadLLC  
**Repository:** `ProjectLaunchPadLLC/Kailos`  
**Status:** Foundational Design / Pre-Implementation  
**Prepared by:** GPT-5.6 Luna (OpenAI / ChatGPT), acting as Master Repository Agent (CG-v1.0)  
**Date:** 2026-09-07

## 1. Core Objective

Create a lightweight computational platform in which the user's existing device becomes the primary compute substrate, while workflows, tools, and persistent state can exist externally and be retrieved only when required.

The platform should eliminate the assumption that every computational application requires a dedicated VPS or continuously running server.

> **Compute locally. Retrieve capabilities as needed. Persist state separately. Use remote compute only when necessary.**

## 2. Core Architecture

```text
                         KAILOS PLATFORM
                               │
                       ┌───────▼───────┐
                       │      CLI      │
                       │   / Web UI    │
                       └───────┬───────┘
                               │
                       ┌───────▼───────┐
                       │ Kailos Runtime│
                       │               │
                       │ Orchestration │
                       │ Execution     │
                       │ Capability    │
                       │ Loading       │
                       │ Provenance    │
                       └───────┬───────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
             Workflows       Tools        Data
             / Manifests   / Packages    / State
                 │             │             │
                 └─────────────┼─────────────┘
                               │
                               ▼
                        CURRENT DEVICE
                      CPU / RAM / Storage
                               │
                               ▼
                         Local execution
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
                Local state        Persistent state
                                   cloud / local
```

## 3. Design Principles

### 3.1 Device-first computation

The device the user is currently operating becomes the default execution environment. A VPS, dedicated server, or permanent cloud runtime is not required when local resources are sufficient.

### 3.2 Lightweight runtime

Kailos should remain as small and efficient as practical. The runtime provides fundamental execution machinery rather than containing every possible capability.

Favor small primitives, composable tools, external workflows, dynamic capability loading, deterministic operations where possible, local execution, and minimal dependencies.

### 3.3 External capabilities

Workflows and tools are independently addressable artifacts. Possible sources include Git repositories, Gists, package repositories, domain-hosted manifests, and other trusted artifact stores.

External availability does **not** imply external execution. A remotely hosted capability can be retrieved, verified, and executed locally.

The minimum lifecycle is:

```text
Discover → Retrieve → Verify → Load → Execute → Cache or discard
```

## 4. Kailos as the Computational Core

Kailos functions as the local reasoning and orchestration component of the runtime. It does not need to perform every operation itself.

```text
User request
     ↓
Kailos
     ↓
Determine required operations
     ↓
Resolve capabilities
     ↓
Execute tools
     ↓
Interpret results
     ↓
Produce result
```

This separates reasoning from deterministic computation.

## 5. Command Abstraction

Users should interact with capabilities through simple commands.

Example:

```bash
kailos run extract-html ./paper.html
```

Internally:

```text
extract-html
     ↓
workflow identifier
     ↓
workflow manifest
     ↓
required tools
     ↓
Kailos runtime
     ↓
local execution
```

The first prototype only needs `kailos run <workflow> <target>`.

## 6. Workflow Manifests

A workflow describes what needs to happen without embedding the entire platform.

```yaml
workflow_id: extract-html
version: 1.0

objective:
  description: Extract structured information from an HTML document.

input:
  type: file
  format: html

tools:
  - html-parser
  - metadata-extractor

execution:
  preferred: local

output:
  type: json

verification:
  required: true
```

The workflow can reside externally. The runtime retrieves it, verifies it, and executes it.

## 7. Persistent State

Compute and storage are separate concerns.

Temporary computation can remain in RAM; small reusable data can be cached locally; persistent state can reside in cloud-native storage or local storage when appropriate; large datasets can remain remote; provenance should be durable.

## 8. Optional Edge Compute

An attached computer can become a Kailos Edge Node. Examples include an old computer, Raspberry Pi, mini-PC, laptop, or other suitable device.

```text
Router
  │
  ├── Phone
  ├── Laptop
  └── Kailos Edge Node
          │
          └── additional compute
```

The user-facing interface remains unchanged; the runtime gains another execution substrate.

## 9. Optional Cloud Execution

Remote execution is an option rather than the foundation. Cloudflare Workers or another execution provider may be used when local resources are insufficient, isolation is desirable, remote execution is required, or temporary scalable compute is advantageous.

```text
                 Task
                  │
                  ▼
             Kailos Runtime
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      Local      Edge      Cloud
      device     node      Worker
```

The workflow remains independent of the execution substrate.

## 10. Domain as Platform Identity

A Kailos domain can provide stable network identity for discovery, routing, workflow manifests, capability metadata, and APIs. The domain itself does not provide computation; the selected execution substrate does.

## 11. Security Requirement

External capabilities must never be blindly executed.

```text
Retrieve
   ↓
Verify identity/version
   ↓
Verify integrity
   ↓
Check authorization
   ↓
Check permissions
   ↓
Execute
```

Secrets must never be stored in public or merely URL-obscured workflow artifacts. Credentials belong in an appropriate secret-management mechanism.

## 12. Provenance

Meaningful executions should be capable of recording an execution ID, workflow ID/version/hash, tool versions/hashes, input identity/hash, runtime version, execution location, result identity/hash, and verification status.

## 13. Minimum Viable Implementation

Do not implement the entire architecture initially. The first milestone proves one complete vertical slice.

### M1 — Local Workflow Execution

Implement:

```bash
kailos run extract-html ./test.html
```

The system must:

1. Accept a workflow identifier.
2. Resolve the workflow.
3. Retrieve its definition.
4. Verify it.
5. Retrieve the required tool.
6. Execute locally.
7. Produce a structured result.
8. Record a basic execution record.

Nothing else is required for M1.

## 14. Iterative Expansion

- **M2 — Multiple Tools:** compose several primitives.
- **M3 — External Workflow Registry:** retrieve workflows from Gists, GitHub, or domain endpoints.
- **M4 — Capability Registry:** discover available tools dynamically.
- **M5 — Persistent Memory:** add local and cloud-backed state.
- **M6 — Provenance:** add complete execution identity and verification.
- **M7 — Web Control Plane:** add a domain-hosted UI.
- **M8 — Cloud Execution:** add ephemeral Cloudflare Worker execution.
- **M9 — Edge Nodes:** allow attached devices to participate as compute nodes.
- **M10 — Distributed Scheduling:** allow Kailos to select the most appropriate execution substrate.

## 15. Architectural Goal

The long-term objective is a small computational fabric capable of assembling useful computation from independently addressable components.

> **The platform supplies execution. External artifacts supply capabilities. Kailos supplies reasoning and orchestration. The user's available hardware supplies compute. Persistent storage supplies memory.**

## 16. Scope Discipline

Every expansion should answer:

1. What capability does this add?
2. What artifact implements it?
3. How is it verified?
4. How is it tested?
5. Why is it necessary now?

The system should continuously return to the smallest executable vertical slice.

> **Explore broadly. Build narrowly. Verify continuously.**

## Initial Success Criterion

The first meaningful proof is that a user can run:

```bash
kailos run extract-html ./test.html
```

on an ordinary device and receive a verified result **without requiring a VPS or permanently installed application-specific server**.
