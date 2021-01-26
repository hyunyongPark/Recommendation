# 작업환경

- segmentation 및 match 알고리즘 코드가 있는 workdir입니다.

```
/home/korea/fashion-recommendation
```

- `dataset` 에 입력파일, 출력파일들이 저장되어 있습니다.
  - For segmentation
    - `samples`: 입력이미지가 저장된 폴더
    - `seg_image`: 입력이미지를 segementation된 이미지로 반환하는 폴더
  - For match recommendation
    - `segDB`: segementation된 이미지들이 저장된 폴더
    - `rec_images`: match된 추천이미지들이 저장된 폴더

# Segmentation

- 해당 코드들은 docker 환경에서 작동됩니다. 컨테이너의 이름은 `seg_rec` 입니다.
- 해당 컨테이너의 동기화된 폴더는 `src`, `script`, `dataset`, `model` 입니다.

1. `seg_rec` 컨테이너 활성화

```
docker start seg_rec
```

2. `seg_rec` 컨테이너 실행

```
docker exec -it seg_rec bash
```

3. 서비스 코드는 `src/serve_seg.py` 이며, 입력이미지와 출력이미지의 경로를 입력해줍니다.

   - 예제) `script/run_serve_seg.sh`

   - ```
     sudo python src/serve_seg.py --image_path ./dataset/samples/056665.jpg --target_category "upper" --save_path ./dataset/seg_images
     ```



# Match

- 랜덤한 이미지에 대해 유사도 기반으로 다른 카테고리(상의 -> 하의 등) 아이템을 추천합니다.
- Segmentation과 동일한 docker 환경에서 수행됩니다.

1. `seg_rec` 컨테이너 활성화

```
docker start seg_rec
```

2. `seg_rec` 컨테이너 실행

```
docker exec -it seg_rec bash
```

3. 서비스 코드는 `src/image2seg.py` 이며,
1) `image_path`: 입력이미지 파일 경로
2) `save_path`: 추천 결과 json파일 결과물 저장 경로
3) `target_category`: 추천 받고자 하는 아이템의 종류(coat, jean, jacket 등) `필수사항` `영어입력`
4) `target_color`: 추천 받고자 하는 아이템의 색상(블랙, 블루 등) `선택사항(default = None)` `한글입력`
5) `target_style`: 추천 받고자 하는 아이템의 스타일(섹시, 스트릿 등) `선택사항(default = None)` `한글입력`
6) `top_k`: 추천 개수

결과물은 /fashion_repo/dataset/rec_images/jsons에 파일(e.g. 049713.json)이 저장이 됩니다.

   - 예제) `script/run_recomm.sh`

   - ```
     sudo sh run_recomm.sh
     ```

   - 예제) `src/image2seg.py`

   - ```
     sudo python src/image2seg.py \
     --image_path ./dataset/samples/055981.jpg \
     --target_category "jean" \
     --target_color "블랙" \
     --target_color "섹시" \
     --save_path ./dataset/rec_images \
     --top_k 5
     ```


# Retrieval Test

- 이미지 유사도 기반 추천에 대한 지표(Recall rate, Hit ratio, MMR)를 출력합니다.

1. `seg_rec` 컨테이너 활성화

```
docker start seg_rec
```

2. `seg_rec` 컨테이너 실행

```
docker exec -it seg_rec bash
```

3. 서비스 코드는 `src/recomm_test.py` 이며,
1) `extractor_path`: cgd_pca.pkl 등 이미지 피쳐 벡터를 생성한 파일 경로 (default: "./dataset/feature_extraction")
2) `extractor_type`: cgd_pca, cgd_res101 등 피쳐 벡터 생성 방법론의 이름 (default: "cgd_pca")
3) `set_ks`: 평가를 원하는 k의 종류로, k가 5인 경우 최대 5개의 아이템을 추천한 후 그 내부에서 지표를 계산 (default: "1,2,5,10,20")