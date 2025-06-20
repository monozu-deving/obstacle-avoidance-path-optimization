### 해당 프로젝트는 경로 탐색을 위한 알고리즘에 대해서 공부하기 위해 제작한 프로젝트 입니다

- GPT4o의 도움을 받아 진행중에 있습니다
- 주요 활용 라이브러리는 pygame으로 출발지, 목적지, 장애물을 설정하면 알고리즘을 기반으로 구동됩니다
- 사용되는 알고리즘의 종류와 갯수는 추후 조사 및 연구 후 확장할 예정입니다.

---

### 📌 1. **그래프 기반 알고리즘 (Graph-based)**

* 경로를 노드와 간선으로 구성된 그래프 상에서 탐색
* **특징**: 명확한 최단거리 탐색, 계산량 예측 가능

| 알고리즘               | 설명                                           |
| ------------------ | -------------------------------------------- |
| **Dijkstra**       | 가중치 있는 그래프에서 출발지로부터 최단 경로를 구함                |
| **A\***            | 휴리스틱(추정 거리)을 이용한 향상된 탐색 알고리즘 (Dijkstra보다 빠름) |
| **D\* / D\* Lite** | 동적인 환경에서도 경로 재탐색 가능                          |
| **Bellman-Ford**   | 음수 가중치 허용, 느리지만 확실                           |

---

### 📌 2. **샘플링 기반 알고리즘 (Sampling-based)**

* 공간을 샘플링하여 경로를 찾는 방법, 특히 고차원 공간에서 유용

| 알고리즘                                    | 설명                         |
| --------------------------------------- | -------------------------- |
| **RRT (Rapidly-exploring Random Tree)** | 무작위 샘플링으로 트리 확장, 빠른 탐색 가능  |
| **RRT\***                               | RRT에 최적화 기능 추가, 더 짧은 경로 생성 |
| **PRM (Probabilistic Roadmap)**         | 미리 맵 전체에 경로 네트워크 구성 후 사용   |

---

### 📌 3. **기하학적 / 최적화 기반 알고리즘**

* 경로를 수식 또는 에너지 최소화 방식으로 최적화

| 알고리즘                                    | 설명                         |
| --------------------------------------- | -------------------------- |
| **Bezier Curve / B-Spline**             | 매끄러운 곡선 경로 생성, 로봇 경로에 적합   |
| **CHOMP / STOMP / TrajOpt**             | 경로를 함수로 보고 에너지를 최소화        |
| **Model Predictive Control (MPC)**      | 동역학 모델 기반의 경로 최적화 및 추적     |
| **Gradient Descent-based Optimization** | cost function을 최소화하는 경로 도출 |

---

### 📌 4. **딥러닝 및 강화학습 기반**

* 복잡한 환경 또는 행동 학습에 적합

| 알고리즘                                     | 설명                           |
| ---------------------------------------- | ---------------------------- |
| **DQN (Deep Q-Network)**                 | 상태-행동 값을 학습하여 최적 행동 도출       |
| **PPO, A3C, SAC 등**                      | 정책 기반 강화학습, 복잡한 행동을 효율적으로 학습 |
| **End-to-End Learning (e.g. imitation)** | 전문가 경로 데이터를 학습하여 경로 추론       |

---

### 📌 5. **하이브리드 알고리즘**

* 여러 방식 조합 (예: 그래프 + 최적화, 샘플링 + 강화학습 등)

예시:

* A\*로 초기 경로 → CHOMP로 매끄럽게 → MPC로 실시간 추적
* PRM + DQN → 복잡한 환경에서 샘플링 기반 정책 탐색
