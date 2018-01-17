# グループ化

import pandas as pd

# 一部の都道府県に関するDataFrameを作成
prefecture_df = pd.DataFrame([["Tokyo", 2190, 13636, "Kanto"], ["Kanagawa", 2415, 9145, "Kanto"],
                              ["Osaka", 1904, 8837, "Kinki"], ["Kyoto", 4610, 2605, "Kinki"],
                              ["Aichi", 5172, 7505, "Chubu"]],
                             columns=["Prefecture", "Area", "Population", "Region"])
# 出力
print(prefecture_df)

# prefecture_dfを地域(Region)についてグループ化し、grouped_regionに代入してください
grouped_region = prefecture_df.groupby("Region")

# prefecture_dfに出てきた地域ごとの、面積(Area)と人口(Population)の平均をmean_dfに代入してください
mean_df = grouped_region.mean()

# 出力
print(mean_df)
