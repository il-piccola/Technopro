import os
import math
import pandas as pd
import numpy as np
import sympy as sp
from geopy.distance import geodesic
from settings import *

# 基準点の角度とΔdの関係を求める

# 基準ポイントA(N37.5.0 E125)の角度データ作成 => E127.5 -> E125 に変更(2022/06/16)
# 距離10　右側(-90°～+90°)
def makeAngleFileA() :
    # 平均距離の設定
    r = 10
    ang = 0

    # 右側180°(-90～+90)
    ang_def = -90

    # 緯度のずらし幅
    delta = 0.1

    # 基準ポイント（緯度・経度）
    stn_N = 37.5
    stn_E = 125

    df1 = pd.DataFrame(columns=["angle","ddA10","N","E"])

    ########################################

    for i in range(1800):
        angle = ang_def + i/10
        df1.loc[i,"angle"] = angle
        
        # 基準を中心に半径rの座標
        nd = r*math.sin(math.radians(angle))
        ed = r*math.cos(math.radians(angle))

        # 緯度。経度から距離を求める
        df1.loc[i,"N"] = nd
        df1.loc[i,"E"] = ed
        # dis1 = geodesic(stn_N + (nd - delta/2) ,stn_E + ed).km
        dis1 = geodesic((stn_N- delta/2 ,stn_E),(stn_N + nd, stn_E + ed)).km
        dis2 = geodesic((stn_N + delta/2,stn_E),(stn_N + nd, stn_E + ed)).km

        # 微調整した距離の差を求める
        dd = dis2 -dis1
        df1.loc[i,"ddA10"] = dd/2044

    #######################################################

    df1.to_csv(os.path.join(WORKDIR, ANGLE_FILE_A))


# 基準ポイントB(N32.5 E125)の角度データ作成
# 距離7　右側(-90°～+90°)
def makeAngleFileB() :
    # 平均距離の設定
    r = 7
    ang = 0

    # 右側180°(-90～+90)
    ang_def = -90

    # 緯度のずらし幅
    delta = 0.1

    # 基準ポイント（緯度・経度）
    stn_N = 32.5
    stn_E = 125

    df2 = pd.DataFrame(columns=["angle","ddB07","N","E"])

    ########################################

    for i in range(1800):
        angle = ang_def + i/10
        df2.loc[i,"angle"] = angle
        
        # 基準を中心に半径rの座標
        nd = r*math.sin(math.radians(angle))
        ed = r*math.cos(math.radians(angle))

        # 緯度。経度から距離を求める
        df2.loc[i,"N"] = nd
        df2.loc[i,"E"] = ed
        dis1 = geodesic((stn_N- delta/2 ,stn_E),(stn_N + nd, stn_E + ed)).km
        dis2 = geodesic((stn_N + delta/2,stn_E),(stn_N + nd, stn_E + ed)).km

        # 微調整した距離の差を求める
        dd = dis2 -dis1
        df2.loc[i,"ddB07"] = dd/2044

    #######################################################

    df2.to_csv(os.path.join(WORKDIR, ANGLE_FILE_B))


# 基準ポイントC(N40.0 E147.5)の角度データ作成
# 距離8　左側(90°～270°)
def makeAngleFileC() :
    # 平均距離の設定
    r = 8
    ang = 0

    # 左側180°(90～270)
    ang_def = 90

    # 緯度のずらし幅
    delta = 0.1

    # 基準ポイント（緯度・経度）
    stn_N = 40
    stn_E = 147.5

    df3 = pd.DataFrame(columns=["angle","ddC08","N","E"])

    ########################################

    for i in range(1800):
        angle = ang_def + i/10
        # df.iloc['行番号','列番号']
        df3.loc[i,"angle"] = angle
        

        nd = r*math.sin(math.radians(angle))
        ed = r*math.cos(math.radians(angle))

        # 緯度。経度から距離を求める
        df3.loc[i,"N"] = nd
        df3.loc[i,"E"] = ed
        dis1 = geodesic((stn_N- delta/2 ,stn_E),(stn_N + nd, stn_E + ed)).km
        dis2 = geodesic((stn_N + delta/2,stn_E),(stn_N + nd, stn_E + ed)).km

        # 微調整した距離の差を求める
        dd = dis2 -dis1
        df3.loc[i,"ddC08"] = dd/2044

    #######################################################

    df3.to_csv(os.path.join(WORKDIR, ANGLE_FILE_C))


# 基準ポイントD(N32.5 E145)の角度データ作成
# 距離10　左側(90°～270°)
def makeAngleFileD() :
    # 平均距離の設定
    r = 10
    ang = 0

    # 左側180°(90～270)
    ang_def = 90

    # 緯度のずらし幅
    delta = 0.1

    # 基準ポイント（緯度・経度）
    stn_N = 32.5
    stn_E = 145

    df4 = pd.DataFrame(columns=["angle","ddD10","N","E"])

    ########################################

    for i in range(1800):
        angle = ang_def + i/10
        df4.loc[i,"angle"] = angle

        nd = r*math.sin(math.radians(angle))
        ed = r*math.cos(math.radians(angle))

        # 緯度。経度から距離を求める
        df4.loc[i,"N"] = nd
        df4.loc[i,"E"] = ed
        dis1 = geodesic((stn_N- delta/2 ,stn_E),(stn_N + nd, stn_E + ed)).km
        dis2 = geodesic((stn_N + delta/2,stn_E),(stn_N + nd, stn_E + ed)).km

        # 微調整した距離の差を求める
        dd = dis2 -dis1
        df4.loc[i,"ddD10"] = dd/2044

    #######################################################

    df4.to_csv(os.path.join(WORKDIR, ANGLE_FILE_D))


# Δｄの値から基準点からＷＰの角度(方向）を見極める処理

# 基準点A(N37.5 E125) ※E127.5 => E125 に変更(2022/06/16)
def find_wp_A_angle(dd = 0):
    angle_path = os.path.join(WORKDIR, ANGLE_FILE_A)
    if not os.path.exists(angle_path) :
        makeAngleFileA()
    df = pd.read_csv(angle_path)
    for i in range(1800):
        d01 = df.loc[i, 'ddA10']
        if d01 -dd < 0:
            answer = df.loc[i, 'angle']
    return answer

# 基準点B(N32.5 E125)
def find_wp_B_angle(dd = 0):
    angle_path = os.path.join(WORKDIR, ANGLE_FILE_B)
    if not os.path.exists(angle_path) :
        makeAngleFileB()
    df = pd.read_csv(angle_path)
    for i in range(1800):
        d01 = df.loc[i, 'ddB07']
        if d01 -dd < 0:
            answer = df.loc[i, 'angle']
    return answer

# 基準点C(N40.0 E147.5)
def find_wp_C_angle(dd = 0):
    angle_path = os.path.join(WORKDIR, ANGLE_FILE_C)
    if not os.path.exists(angle_path) :
        makeAngleFileC()
    df = pd.read_csv(angle_path)
    for i in range(1800):
        d01 = df.loc[i, 'ddC08']
        if d01 -dd > 0:
            answer = df.loc[i, 'angle']
    return answer

# 基準点D(N32.5 E145)
def find_wp_D_angle(dd = 0):
    angle_path = os.path.join(WORKDIR, ANGLE_FILE_D)
    if not os.path.exists(angle_path) :
        makeAngleFileD()
    df = pd.read_csv(angle_path)
    for i in range(1800):
        d01 = df.loc[i, 'ddD10']
        if d01 -dd > 0:
            answer = df.loc[i, 'angle']
    return answer


# ２点の基準ポイントからの角度から交点の座標を求める
# 基準Aを（N37.5,E125)に変更　旧は(E127.5)

# 関数定義 find_wp_from_stAngle(基準点st1("A,B,C,D") , Angle,基準点st2("A,B,C,D"),Angle2）
def find_wp_from_stAngle(st1="a", Angle1=0, st2="b", Angle2=0):
    
    if st1 == "a" or st1 == "A" :
        # 基準点A (N37.5 E125)
        X1 = NE_A[1]
        Y1 = NE_A[0]
    
    if st1 == "b" or st1 == "B" :
        # 基準点B (N32.5 E125)
        X1 = NE_B[1]
        Y1 = NE_B[0]

    if st1 == "c" or st1 == "C" :
        # 基準点C (N40 E147.5)
        X1 = NE_C[1]
        Y1 = NE_C[0]

    if st1 == "d" or st1 == "D" :
        # 基準点D (N32.5 E145)
        X1 = NE_D[1]
        Y1 = NE_D[0]

    ####################
    if st2 == "a" or st2 == "A" :
        # 基準点A (N37.5 E125)
        X2 = NE_A[1]
        Y2 = NE_A[0]

    if st2 == "b" or st2 == "B" :
        # 基準点B (N32.5 E125)
        X2 = NE_B[1]
        Y2 = NE_B[0]

    if st2 == "c" or st2 == "C" :
        # 基準点C (N40 E147.5)
        X2 = NE_C[1]
        Y2 = NE_C[0]

    if st2 == "d" or st2 == "D" :
        # 基準点D (N32.5 E145)
        X2 = NE_D[1]
        Y2 = NE_D[0]

    #傾きを求める
    a1 = np.round(np.tan(Angle1* np.pi/180),decimals= 5)
    a2 = np.round(np.tan(Angle2* np.pi/180),decimals= 5)
    #切片を求める
    b1 = -1*a1*X1 + Y1
    b2 = -1*a2*X2 + Y2
    #1次関数2つの連立方程式を解く
    x, y = sp.symbols('x, y')
    eq1 = sp.Eq(-1*a1*x + 1*y, b1)
    eq2 = sp.Eq(-1*a2*x + 1*y, b2)
    solve = sp.solve([eq1, eq2], [x, y])
    X = solve[x]
    Y = solve[y]

    return X, Y


