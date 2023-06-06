# -*- coding: utf-8 -*-

import proto
import torch

if __name__ == "__main__" : 
    device = torch.device('cuda')

    model = proto.load_protonet_vit(
        in_channels=1,  # 입력 채널 수
        patch_size=[16, 64],  # 패치 크기 (세로, 가로)
        embed_dim=64,  # 임베딩 차원
        num_layers=12,  # Transformer 블록 수
        num_heads=8,  # 멀티헤드 어텐션에서의 헤드 수
        mlp_dim=4,  # MLP의 확장 비율
        num_classes=4,  # 분류할 클래스 수
        in_size=[64, 64]  # 입력 이미지 크기 (가로, 세로)
    )
    model.load_state_dict(torch.load('model.pt', map_location=device))

    print(model)