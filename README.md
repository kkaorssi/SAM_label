# Segment Anything Model (SAM) 기반 이미지 레이블링 도구
## Overview
이 프로젝트는 Meta AI에서 개발한 **Segment** **Anything** **Model** (SAM)을 기반으로 이미지에 레이블링 작업을 도와주는 도구입니다.
**PyQt5**를 사용하여 사용자 인터페이스(UI)를 구축하였으며, 사용자는 이 도구를 통해 이미지를 불러오고, SAM을 적용하여 자동으로 세그먼트된 영역을 생성한 후, 이를 기반으로 레이블링 작업을 수행할 수 있습니다.

## Key Features
- 이미지 불러오기: 사용자가 로컬 디스크에서 이미지를 불러올 수 잇습니다.
- SAM 모델 적용: 불러온 이미지에 SAM 모델을 적용하여 자동을 세그먼트된 영역을 생성합니다.
- 세그먼트 편집: 생성된 세그먼트를 수정하거나, 추가로 영역을 선택하여 레이블링 작업을 수행할 수 있습니다.
- 레이블링: 각 세그먼트에 레이블을 할당하고, 결과를 저장할 수 있습니다.
- 저장 및 불러오기: 레이블링 작업이 완료된 이미지를 저장하거나, 이전에 작업한 결과를 불러올 수 있습니다.
- 기능 개발 예정:
    - Auto Mode: SAM의 Auto Mode를 적용할 수 있도록 업데이트 예정입니다.
    - Undo/Redo: 작업 내역을 취소(Undo)하거나 다시 실행(Redo)할 수 있는 기능이 추가될 예정입니다.

## Run Video
<img src="https://github.com/user-attachments/assets/4cdb433f-4886-4756-8aaf-01663e8f6299">
 
## License
이 프로젝트는 Apache License 2.0에 따라 배포됩니다.
