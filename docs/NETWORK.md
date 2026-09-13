# Network target

Antibody is locked to GenLayer **Studionet**, the stable hosted Studio environment.

| Setting | Value |
|---|---|
| Network | Studionet |
| Chain ID | `61999` |
| RPC | `https://studio.genlayer.com/api` |
| Explorer | `https://explorer-studio.genlayer.com` |
| Currency | GEN |

`gltest.config.yaml` exposes the network as `studionet`.

`scripts/deploy_studionet.py` sends an `eth_chainId` request to the configured RPC and aborts unless the result is exactly `61999`. It then deploys with the explicit RPC instead of mutating or trusting a saved default network.
