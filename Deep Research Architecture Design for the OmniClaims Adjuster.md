Architecture Design for the OmniClaims Adjuster: Transforming Insurance Adjudication via Autonomous Multimodal Google Gemini Agents

The insurance industry faces an operating environment of unprecedented complexity in the 2024-2025 biennium. While 92% of organizations have invested in artificial intelligence, 78% of projects have failed or stalled due to the systems' inability to handle the multidimensional and fragmented nature of enterprise data.[1] Bottlenecks in sectors such as human resources, logistics, and sales are significant, but it is in the insurance domain where the convergence of extensive legal documents, critical visual evidence, and the need for deep causal reasoning creates a "perfect storm" scenario that only a technology with Google Gemini's capabilities can resolve.[2, 3, 4] This report details the design of the OmniClaims Adjuster, an autonomous agent engineered to win the "Best Use of Gemini" award by integrating massive context windows, native multimodality, and agentic workflows to redefine claims adjudication.

Evaluation of Sectoral Bottlenecks and Problem Selection

To determine the use case with the highest potential return on investment (ROI) and technological differentiation, it is imperative to analyze the operational friction across the four key sectors identified.

Analysis of Friction in Human Resources and Sales

In the Human Resources sector, bottlenecks concentrate on talent acquisition and pay equity management. Organizations struggle with weak job architectures that do not allow objective comparisons between roles, leading to gender gaps and difficulties complying with European Union pay transparency directives.[5] Although interview video analysis and resume screening benefit from AI, the impact is often incremental and limited by ethical and bias concerns that require constant human supervision.[6, 7, 8] On the other hand, in the Sales area, the primary challenge lies in personalization at scale and the management of complex presales processes, such as responding to RFPs (Request for Proposals). While Gemini can process thousands of pages of technical documents, the transactional nature of sales often depends more on human relationships than on pure data processing.[4, 9]

Critical Challenges in Logistics and Supply Chain

Logistics faces disruptions costing approximately $184 billion annually on a global level.[10] Bottlenecks here are both physical and digital: port congestion, material shortages, and an excessive reliance on legacy systems that do not communicate with each other.[11, 12, 13] AI in logistics is used for route optimization and predictive maintenance, but the integration of autonomous agents often clashes with the rigidity of physical infrastructure and safety risks associated with direct machine-to-human interaction.[11, 14]

The Insurance Sector: The Optimal Use Case for Gemini

The insurance sector presents the highest density of inefficiencies that align perfectly with the exclusive capabilities of Gemini. Claims adjudication is a time-consuming, human-error-prone, and extremely costly process. Manual processing of a standard claim takes between 70 minutes and several hours of active labor, with an administrative cost close to $50 per file.[15] Average cycle times from the First Notice of Loss (FNOL) to the final payment exceed 30 days, causing a drastic drop in customer satisfaction.[15, 16, 17]

The complexity of insurance lies in the fact that a single claim requires:
- Deep understanding of hundreds-of-pages legal policies (Long Context Window).
- Analysis of evidence in multiple formats: damage photos, dashcam accident videos, audio recordings of statements, and scanned medical invoices (Native Multimodality).
- Multi-step orchestration: coverage verification, fraud detection, damage estimation, and payment issuance (Agentic Workflows).

Due to this unique convergence of needs, the selected problem for the solution is Auto-Claims Adjudication. This use case not only demonstrates Gemini's technical superiority but also offers a radical business impact, reducing operating costs by up to 50% and improving fraud detection accuracy to 95%.[18, 19]

| Sector | Main Bottleneck | Gemini Potential | Selection Justification |
| :--- | :--- | :--- | :--- |
| **HR** | Subjective evaluation and pay gaps. | Interview and resume analysis. | High ethical risks and moderate ROI.[5, 7] |
| **Logistics** | Route disruption and data silos. | Network optimization and cargo vision. | Reliance on rigid physical infrastructure.[10, 11] |
| **Sales** | Slow RFP response and lack of personalization. | Processing technical documents. | Impact limited by the human factor.[4, 9] |
| **Insurance** | Slow payment cycles and undetected fraud. | Multimodal reasoning over policies and evidence. | Maximum utilization of all exclusive capabilities.[3, 18] |

Agent Architecture: The OmniClaims Adjuster

The OmniClaims Adjuster is a system of interconnected autonomous agents, built on the Gemini Enterprise Agent Platform, which transforms the linear adjudication process into a dynamic, goal-oriented workflow.[20, 21] The architecture is divided into three fundamental layers: Multimodal Ingestion, Reasoning Orchestration, and Action Execution.

Multimodal Ingestion and Perception Layer

The workflow begins when the insured initiates a claim through any channel (mobile app, web portal, or phone call). The agent is designed to receive a massive and unstructured inflow of data.
- **Audio Inputs**: Utilizing the Gemini Live API, the agent can process phone calls in real time, detecting not only words but also the emotional tone (affective dialog) to offer an empathetic response while extracting structured data.[22, 23, 24]
- **Video and Image Inputs**: The agent receives dashcam videos or smartphone recordings of the incident scene. Gemini 1.5 Pro analyzes these videos frame by frame to reconstruct the sequence of events, determine the relative speed of the vehicles, and assess the severity of the impact.[25, 26, 27]
- **Documentary Inputs**: The system ingests police reports in PDF, medical histories, and the customer's full policy, leveraging the context window of over one million tokens to keep all information available during reasoning.[25, 28]

Orchestration and Reasoning (Agentic Workflow)

Once the data is in the system, the Supervisor Agent (Orchestrator) uses the Agent Development Kit (ADK) to plan the resolution of the case. The workflow is not a rigid sequence, but an iterative "Plan-Execute-Review" thought process.[29]
- **Identity and Coverage Verification**: The agent invokes a database function to retrieve policy terms. It utilizes long-context reasoning to compare the reported incident with exclusion clauses and coverage limits.[25, 30, 31]
- **Multimodal Evidence Analysis**: The task is delegated to a specialized vision sub-agent. This agent compares damage photos with the accident video to ensure the claimed damages are consistent with the observed dynamics of the impact.[32, 33]
- **Fraud and Risk Investigation**: An "Anomaly Hunting" agent uses Gemini Embedding 2 to compare the current incident against a database of known fraud patterns. By mapping text, video, and audio into the same semantic space, the agent identifies discrepancies that traditional rules-based systems would miss.[28, 34]
- **Triage and Decision**: If the case has low complexity and high confidence (Straight-Through Processing), the agent generates an immediate payment recommendation. If "red flags" or missing information are detected, the agent autonomously contacts the customer to request clarifications or escalates the case to a human adjuster with an executive summary highlighting friction points.[15, 23, 35]

Execution and Output Layer

The system's output is multidimensional, adapting to the needs of different stakeholders.
- **For the Insured**: A rapid resolution, explained in natural language, sent via email or communicated via voice, detailing what was covered and why.[15, 35]
- **For the Core System (System of Record)**: A structured JSON object with all validated claim fields, ready for payment issuance through financial APIs.[30, 36, 37]
- **For the Human Adjuster**: A "Handoff Package" including transcripts, video analysis with timestamps of critical moments, and direct quotes from the policy justifying the decision.[23, 38]

| Workflow Step | Input | Tool/Model | Expected Output |
| :--- | :--- | :--- | :--- |
| **FNOL Ingestion** | Call audio / Photos. | Gemini Live API / 1.5 Pro. | Identity data and initial description.[23] |
| **Policy Analysis** | 500+ page manual. | Gemini 1.5 Pro (Long Context). | Determination of coverage and deductibles.[28] |
| **Damage Assessment** | Dashcam video. | Gemini 1.5 Pro (Multimodal). | Estimation of severity and root cause.[26] |
| **Fraud Validation** | Claim history. | Gemini Embedding 2. | Risk scoring and anomaly detection.[28] |
| **Resolution** | Accumulated context. | Agent Engine / Function Calling. | Payment approved or escalation with summary.[35] |

Specific Use of Gemini's Exclusive Capabilities

The design of the OmniClaims Adjuster would not be possible with traditional language models. Gemini's architecture allows solving problems that previously required dozens of small models and expensive integrations.

Massive Context Window: Holistic Understanding of the Contract

In insurance, "the devil is in the details" of the policy. Traditional RAG systems often fail because they split documents into chunks, losing the connection between a coverage clause on page 5 and a hidden technical exclusion on page 150. Gemini 1.5 Pro, with its capability to process up to 2 million tokens, allows loading not just the customer's policy but also repair manuals, local traffic codes, and the entire history of the insured in a single call.[25, 39, 40]

This "reasoning over the full document" capability ensures that the agent never ignores a critical clause. During the hackathon, this will be demonstrated by loading a 400-page PDF of a commercial policy and asking the agent to identify whether a "burst pipe" damage is covered under specific weather conditions mentioned in a technical appendix. The model's accuracy in fact retrieval (needle-in-a-haystack) is 99%, even with massive data volumes.[25]

Native Multimodality: The Adjuster that "Sees" and "Hears"

Unlike other models that depend on external OCR services or transcription models that lose emotional context, Gemini is multimodal from its inception.[2, 25] This is vital for:
- **Accident Analysis**: The agent can "see" a crash video and understand that the traffic light was red for the claimant, comparing this visual information with the audio testimony.[26, 32]
- **Document Integrity**: The agent detects if a medical invoice has been digitally manipulated by comparing pixel styles with the rest of the document (a type of visual-forensic reasoning that traditional OCRs do not possess).[3, 38]
- **Behavioral Fraud Detection**: Through the Live API, the agent analyzes micro-hesitations and voice tone during claim reporting. If there is a significant discrepancy between the reported calm and vocal agitation, the agent flags the case for additional review.[22, 23]

Agentic Workflows: Autonomy with Causal Reasoning

The OmniClaims Adjuster is not a chatbot; it is a resolving agent. Thanks to the Vertex AI Agent Engine, the model can plan complex sequences of actions.[21, 41] For example, if the agent determines that an appraisal of a damaged property is needed, it can:
- Consult the availability of external appraisers using a calendar API.[42, 43]
- Utilize Google Earth Engine to verify if there were hail storms reported in that exact location at the time of the incident, crossing geospatial data with the claim.[36, 44, 45]
- Generate an inspection order with exact GPS coordinates and reference photos extracted from the customer's initial video.[46, 47]

This capability to orchestrate external tools transforms Gemini from a text generator to an enterprise "decision engine."

Business Impact and Return on Investment (ROI)

The implementation of the OmniClaims Adjuster generates radical improvements across three critical dimensions: operating cost, cycle time, and financial accuracy.

Cost Reduction and Operational Efficiency

The average cost of manually processing a claim is $50 USD. Using Gemini reduces this cost to approximately $0.07 USD per file when using the automated workflow.[15] This efficiency allows insurers to scale their processing capacity without increasing headcount, which is crucial during natural disasters when claim volumes spike suddenly.[12, 19, 48]

| Metric | Manual Process | OmniClaims Adjuster | Improvement |
| :--- | :--- | :--- | :--- |
| **Cycle Time (FNOL to Payment)** | 32.4 days (average) [16] | < 10 days (target) [15, 17] | ~70% reduction |
| **Cost per Claim** | $50.00 USD [15] | $0.07 USD (compute) [15] | >99% OPEX savings |
| **Automation Rate (STP)** | 35% (industry) [18] | 70% - 80% [17, 18] | 2x operational capacity |
| **Extraction Accuracy** | 70% - 80% (traditional OCR) [3] | 98% (Gemini) [3] | 25% improvement in integrity |

Accuracy in Fraud Detection and Payment Leakage

"Claim leakage," which includes overpayments and calculation errors, represents between 5% and 10% of an insurer's premium revenue. Gemini's capability to perform multimodal cross-validation allows identifying fraud patterns with 95% accuracy, far exceeding rule-assisted human detection capacity (which typically hovers around 20-30%).[18]

Enhancement of Customer Experience (NPS)

Customer satisfaction in insurance is directly correlated with payment speed. NPS scores drop from 762 to 595 if the process exceeds 31 days.[15] By reducing response times to minutes or days, the OmniClaims Adjuster not only saves money but also becomes a massive customer retention tool, allowing insurance brands to compete on service rather than just price.[17, 18]

Conclusion and Differentiating Value for the Hackathon

The OmniClaims Adjuster is the winning solution for the "Best Use of Gemini" award because it does not simply try to "do the same thing faster." Instead, it redefines the nature of insurance adjudication work using Google Cloud's three competitive advantages:
- **Cognitive Scale**: No other model can "read" the entire policy and the customer's history simultaneously with the same fidelity as Gemini Pro.[25]
- **Unified Perception**: The capability to reason directly over an accident video without intermediate data conversion steps reduces latency and translation errors.[25, 26]
- **Ecosystem Integration**: The solution leverages Vertex AI infrastructure to guarantee security, governance (Agent Gateway), and observability (Unified Trace Viewer), elements that insurers demand before deploying any AI in production.[20, 21, 49]

This proposal is not just a theoretical vision; it is a viable architecture that utilizes GA (General Availability) and Preview tools from 2024-2025 to solve a billion-dollar problem, demonstrating that Gemini is the engine of the next generation of autonomous enterprises.[36, 50, 51] By automating the heaviest, most technical part and proposing a multimodal workflow, the OmniClaims Adjuster allows humans to focus on the cases of highest sensitivity and complexity, humanizing technology where it matters most.[2, 19]

--------------------------------------------------------------------------------

[1] 92% of organizations have invested in AI but 78% say projects have either stalled or failed, https://www.prnewswire.com/news-releases/92-of-organizations-have-invested-in-ai-but-78-say-projects-have-either-stalled-or-failed-302769202.html
[2] Real-World Multimodal AI Use Cases | Rasa Blog, https://rasa.com/blog/multimodal-ai-use-cases
[3] MediConCen case study - Google Cloud, https://cloud.google.com/customers/mediconcen
[4] Cloud for insurance and financial services | Google Cloud, https://cloud.google.com/solutions/financial-services/insurance
[5] 5 Human Resources Trends to Watch in 2025 - Aon, https://www.aon.com/en/insights/articles/five-human-resources-trends-to-watch-in-2025
[6] Google AI for HR Teams, https://workspace.google.com/solutions/ai/hr/
[7] AI Video Interviewing for Faster Hiring & Smarter Talent Decisions - Phenom, https://www.phenom.com/blog/ai-video-interviewing
[8] AI-Powered HR Recruitment Management System with Resume Screening, Interview Automation, Video Assessment and Candidate Skill Gap Analysis - IJFMR, https://www.ijfmr.com/papers/2025/6/63309.pdf
[9] ‎Gemini Apps' release updates & improvements, https://gemini.google/release-notes/
[10] The Top 10 Supply Chain Risks of 2026 and How to Mitigate Them - NetSuite, https://www.netsuite.com/portal/resource/articles/inventory-management/supply-chain-risks.shtml
[11] AI trends 2025: Adoption barriers and updated predictions - Deloitte, https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/blogs/pulse-check-series-latest-ai-developments/ai-adoption-challenges-ai-trends.html
[12] AI Agents for Logistics and Supply Chain: Complete Guide - MindStudio, https://www.mindstudio.ai/blog/logistics-supply-chain
[13] What are the Impacts of AI on the Logistics Industry : r/AI_in_logistics - Reddit, https://www.reddit.com/r/AI_in_logistics/comments/1ni73ij/what_are_the_impacts_of_ai_on_the_logistics/
[14] Industry Insights: AI in Logistics | Reshaping How Goods Move Globally, https://www.automate.org/ai/industry-insights/ai-in-logistics-and-supply-chain
[15] 5 Principles of Effective Claims Handling in the AI Era (2026 Update) - Decerto, https://www.decerto.com/us/post/5-principles-of-effective-claims-handling-in-the-insurance-industry
[16] How to Reduce Claims Cycle Time with Spatial Documentation - Matterport, https://matterport.com/blog/claims-cycle-time
[17] How to Optimize Insurance Claims Process Flow: Digital Transformation Strategies - Bank Shot, https://www.getbankshot.com/blog-posts/how-to-optimize-insurance-claims-process-flow-digital-transformation-strategies
[18] Claims Team Efficiency Metrics: 40+ Key Statistics Every Insurance Professional Should Know in 2025 - Talli Insights, https://blog.talli.ai/claims-team-efficiency-metrics/
[19] The ROI of Mapping and Optimizing Insurance Back Office Processes - Boost USA, https://boost-usa.com/blog/optimizing-back-office-processes-insurance/
[20] Introducing Gemini Enterprise Agent Platform | Google Cloud Blog, https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform
[21] Vertex AI Agent Builder: 2026 guide to Google's enterprise AI agent platform - UI Bakery, https://uibakery.io/blog/vertex-ai-agent-builder
[22] Gemini Live — Part 1: Building a low-latency, telephone Voice Agent with FreeSWITCH and ADK agents powered by Gemini Live. | by Olejniczak Lukasz | Google Cloud - Medium, https://medium.com/google-cloud/gemini-live-part-1-building-a-low-latency-telephone-voice-agent-with-freeswitch-and-adk-agents-ceafd209f017
[23] Build a Voice-First Insurance Claim Live Agent Team - unwind ai, https://www.theunwindai.com/p/build-a-voice-first-insurance-claim-live-agent-team
[24] Gemini Live API overview - Google AI for Developers, https://ai.google.dev/gemini-api/docs/live-api
[25] Gemini 1.5 Pro - Prompt Engineering Guide, https://www.promptingguide.ai/models/gemini-pro
[26] A Vision-Language Benchmark for Video Question Answering and Dense Captioning for Accident Scene Understanding, https://openaccess.thecvf.com/content/ICCV2025W/2COOOL/papers/Kim_VRU-Accident_A_Vision-Language_Benchmark_for_Video_Question_Answering_and_Dense_ICCVW_2025_paper.pdf
[27] GitHub - MiChaelinzo/CrashScope-AI: "Advanced AI to analyze traffic incidents, providing rapid, precise accident reconstruction using Gemini 1.5 pro technology.", https://github.com/MiChaelinzo/CrashScope-AI/
[28] Building with Gemini Embedding 2: Agentic multimodal RAG and ..., https://developers.googleblog.com/building-with-gemini-embedding-2/
[29] Backend Python Developer (AI-Native) at Novakid - Remocate, https://www.remocate.app/jobs/backend-python-developer-ai-native
[30] Function calling with the Gemini API - generateContent API | Google AI for Developers, https://ai.google.dev/gemini-api/docs/function-calling
[31] How to Implement Function Calling with the Gemini API in Vertex AI - OneUptime, https://oneuptime.com/blog/post/2026-02-17-how-to-implement-function-calling-with-the-gemini-api-in-vertex-ai/view
[32] New AI Language-Vision Models Transform Traffic Video Analysis to Improve Road Safety, https://engineering.nyu.edu/news/new-ai-language-vision-models-transform-traffic-video-analysis-improve-road-safety
[33] Automating Crash Diagram Generation Using Vision-Language Models: A Case Study on Multi-Lane Roundabouts - arXiv, https://arxiv.org/html/2604.15332v1
[34] Get multimodal embeddings | Gemini Enterprise Agent Platform, https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-multimodal-embeddings
[35] Reimagining the Insurance System Architecture with Agentic AI, https://www.tcs.com/what-we-do/products-platforms/tcs-bfsi-platforms/white-paper/reimagining-insurance-system-architecture-agentic-ai
[36] Insurance claim processing reference architecture | Google Cloud ..., https://cloud.google.com/blog/topics/financial-services/insurance-claim-processing-reference-architecture
[37] Automate utilization-review of health insurance claims using generative AI, https://docs.cloud.google.com/architecture/use-generative-ai-utilization-management
[38] Best Insurance Claims Processing OCR Software - LlamaIndex, https://www.llamaindex.ai/insights/best-insurance-claims-processing-ocr-software
[39] Experimenting with Gemini 1.5 Pro and vulnerability detection | Google Cloud Blog, https://cloud.google.com/blog/products/identity-security/experimenting-with-gemini-1-5-pro-and-vulnerability-detection
[40] Our next-generation model: Gemini 1.5 - Google Blog, https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/
[41] Vertex AI Agent Engine - Google Cloud - Medium, https://medium.com/google-cloud/ai-agents-8eb2b6edea9b
[42] Integrate Vertex AI Agents with Google Workspace, https://codelabs.developers.google.com/vertexai-gws-agents
[43] Gemini 3 in Healthcare: An Analysis of Its Capabilities - IntuitionLabs, https://intuitionlabs.ai/articles/gemini-3-healthcare-applications
[44] Delos Insurance Solutions case study | Google Cloud, https://cloud.google.com/customers/delos
[45] Seamlessly integrate Google Earth Engine with CARTO Workflows, https://carto.com/blog/seamlessly-integrate-google-earth-engine-carto-workflows/
[46] Geospatial solutions and analytics - Google Maps Platform, https://mapsplatform.google.com/intl/en_uk/maps-products/geospatial-analytics/
[47] Earth Engine raster analytics and visualization in BigQuery geospatial | Google Cloud Blog, https://cloud.google.com/blog/products/data-analytics/earth-engine-raster-analytics-and-visualization-in-bigquery-geospatial
[48] Harnessing automation and AI for seamless claims processing - Gemini Solutions, https://www.geminisolutions.com/case-studies/harnessing-automation-and-ai-for-seamless-claims-processing-and-fraud-detection
[49] Welcome to Google Cloud Next26, https://cloud.google.com/blog/topics/google-cloud-next/welcome-to-google-cloud-next26
[50] Google Cloud Next '26: Delivering the Agentic Control Plane | TWIML, https://twimlai.com/articles/google-cloud-next-26-recap
[51] Case studies - Google AI Studio, https://aistudio.google.com/case-studies
