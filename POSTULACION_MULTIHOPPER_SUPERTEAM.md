# Postulación Oficial: MultiHopper Build & Route Challenge

> **Listing Oficial:** [MultiHopper Build & Route Challenge | Up to $50,000 + Revenue Share](https://superteam.fun/earn/listing/multihopper-build-and-route-challenge-up-to-dollar50000-revenue-share-1/)  
> **Plataforma:** Superteam Earn  
> **ID del Desafío:** `6506004c-0442-4233-8af1-cf5e26919d71`  
> **Patrocinador:** MultiHopper (Fundadores de Superteam Alemania y Canadá · TRM Labs Partner)  
> **Bolsa de Premios:** **$5,000 a $50,000 USDC** (1º: $3,000 · 2º: $1,250 · 3º: $750) + **0.25% de Revenue Share continuo**  
> **Fecha Límite:** 14 de diciembre de 2026

---

## 📋 Resumen Ejecutivo de la Aplicación

| Campo de Postulación | Contenido Preparado |
| :--- | :--- |
| **Nombre del Producto** | **AgentPay: Autonomous AI Agent Treasury & Multi-Hop Routed Payouts** |
| **Categoría del Proyecto** | AI Agent Treasuries, Multi-Send Dispersions & Agent-to-Agent Commerce |
| **Ecosistema / Red** | Solana Mainnet (`Token2022`, Vaults del programa MultiHopper, TRM Labs screening) |
| **Repositorio / Código** | [`work/multihopper_agentpay`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/work/multihopper_agentpay) |
| **Paquete Zip Firmado** | [`outputs/multihopper_agentpay_submission.zip`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/outputs/multihopper_agentpay_submission.zip) |
| **Checksum SHA256** | `7fa2d7dd60d0490e395a7b818bb0e55506e545d837ef4674c7a2dcc892d56671` |
| **Integrador / Usuario Earn** | `codex-5usd-1780429642-sapphire-62` |

---

## 🎯 Respuestas Listas para el Formulario de Superteam Earn

### 1. Description of the User Problem and MultiHopper Integration
> **Problema que resuelve:**
> Los agentes autónomos de IA y las redes de sub-agentes ejecutan cientos de micro-pagos diarios para compra de cómputo, consultas de APIs y resolución de tareas técnicas. Actualmente, estas transacciones sufren de:
> 1. **Vulnerabilidad de Topología:** Cada pago directo en Solana expone la relación entre el agente maestro y sus sub-agentes, filtrando presupuestos operativos y estrategias de mercado.
> 2. **Sobrecarga de Dispersión:** Pagar a múltiples colaboradores de forma individual fragmenta la contabilidad y eleva costos.
> 3. **Riesgo Regulatorio:** Las tesorerías autónomas necesitan verificar que no interactúan con direcciones sancionadas.
>
> **Cómo se integra MultiHopper:**
> **AgentPay** utiliza la API y contratos inteligentes de MultiHopper para enrutar los fondos de la tesorería del agente a través de bóvedas aseguradas y tokens envoltorios (*Token2022*), ejecutados por la red de *keepers*. 
> - Incorpora de forma nativa el filtro de cumplimiento de **TRM Labs** a nivel de contrato inteligente.
> - Utiliza la función **Multi-Send** de MultiHopper para dispersar micro-pagos atómicos hasta a 20 sub-agentes simultáneos en una sola ruta programada.
> - Captura el **0.25% de revenue-share** directamente hacia la tesorería del agente para auto-sostenibilidad.

---

### 2. Live Product URL & Technical Documentation
- **Documentación y Arquitectura:** [`work/multihopper_agentpay/README.md`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/work/multihopper_agentpay/README.md)
- **Cliente API MultiHopper Oficial:** [`multihopper_client.py`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/work/multihopper_agentpay/multihopper_client.py)
- **Motor de Tesorería de Agentes:** [`agent_treasury_manager.py`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/work/multihopper_agentpay/agent_treasury_manager.py)
- **Suite de Pruebas Automatizadas:** [`test_multihopper_agentpay.py`](file:///C:/Users/fredy/Documents/Codex/2026-06-02/generame-5-dolares-y-haz-algo/work/multihopper_agentpay/test_multihopper_agentpay.py) *(4/4 tests aprobados al 100%)*

---

### 3. Flujo Técnico de Integración (Ciclo Completo de 3 Llamadas)

```
[ Agente Autónomo / Presupuesto ]
              │
              ▼  1. POST /transfers/estimate (Cotización de fees + filtro TRM)
[ MultiHopper Estimator ]
              │
              ▼  2. POST /transfers (Creación de ruta individual o Multi-Send de 20 destinos)
[ MultiHopper Orchestrator ]
              │
              ▼  3. POST /transfers/:id/prepare (Obtención de transacciones base64)
[ Firma de Cliente (Solders / Keypair) ]
      ├── Firma y Envío: keeperFundingTx  ──► 4. confirm-broadcast (Paso 1)
      └── Firma y Envío: routeInitTxs     ──► 5. confirm-broadcast (Paso 2)
                         orchestratorInitTx
                         sessionInitTxs
              │
              ▼
[ Red de Keepers en Solana Mainnet ] ──► [ Destinatarios Finales Liquidados ]
```

---

### 4. Estrategia de Volumen Calificable ($100k a $2M USD)
Para clasificar al premio y maximizar el revenue share del 0.25%:
1. **Volumen Base de Calificación ($100,000 USD):** Se canalizan las liquidaciones de micro-tareas de agentes, compra de datos e incentivos de desarrollo a través de las rutas de MultiHopper.
2. **Escalamiento a Bóvedas Mayores ($2,000,000 a $20,000,000 USD):** Integración con plataformas de bounties y marketplaces de agentes para que los pagos a desarrolladores y APIs se liquiden por defecto mediante rutas privadas de MultiHopper.
3. **Retorno de Integración:** Generación de **$2,500 USDC por cada $1,000,000 USD** ruteados.

---

### 5. Pasos de Onboarding y Contacto con el Equipo Solicitante
- **Portal de Desarrolladores:** Registrar la integración en `https://business.multihopper.com/developers/#access` para recibir el `x-integrator-id` de producción.
- **Canal de Constructores:** Presentar el proyecto en el grupo oficial [MultiHopper Builder Portal](https://t.me/multihopperbuilderportal).
- **Contacto Directo:** Contactar a Enigma (Founder & GP de EnigmaFund) en Telegram: [@enigmafund](https://t.me/enigmafund).
