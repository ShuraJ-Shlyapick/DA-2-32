import pandas as pd
import numpy as np
"""
Задача DA-2-32:
Создание бинарного признака "индекс роста/падения" для временного ряда.
(1) если значение выросло, (0) если упало или не изменилось
"""

def gen_synt_data(n_points=10, seed=None):
    """
    Генерирует синтетический временной ряд.

    Args:
        n_points (int): количество точек данных.
        seed (int, optional): значение для фиксации генератора случайных чисел.

    Returns:
        pd.DataFrame: датафрейм с временным рядом
    """
    if not isinstance(n_points, int) or n_points <= 0:
        raise ValueError(f"n_points must be positive integer, got '{n_points!r}' ")
    try:
        if seed is not None:
            np.random.seed(seed)
        values = np.random.randint(50,150, size=n_points)
        df = pd.DataFrame({
            "time": range(1,n_points + 1),
            "value": values
        })
        return df
    except Exception as e:
        raise RuntimeError(f"Data generation error: {e}")
    
def create_grow_flag(df, column_name):
    """
    Создаёт бинарный признак роста/падения на основе временного ряда.

    Args:
        df (pd.DataFrame): входной датафрейм.
        column_name (str): название столбца с числовыми значениями.

    Returns:
        pd.DataFrame: датафрейм с добавленным бинарным столбцом 'growth_flag'
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' is missing from dataframe.")
    df = df.copy()
    df["diff"] = df[column_name].diff()
    df["growth_flag"] = (df["diff"] > 0).astype(int)
    df["growth_flag"] = df["growth_flag"].fillna(0)
    return df

def calc_growth(df):
    """
    Считает долю случаев, когда значение выросло.

    Args:
        df (pd.DataFrame): датафрейм с бинарным столбцом 'growth_flag'.

    Returns:
        float: доля ростов (от 0 до 1)
    """
    if "growth_flag" not in df.columns:
        raise ValueError(f"Where is no 'growth_flag' column in DataFeame.")
    return df["growth_flag"].mean()

def main():
    try:
        n_points = 10
        df = gen_synt_data(n_points=n_points, seed=42)
        df = create_grow_flag(df, "value")
        growth_share = calc_growth(df)
        print(df)
        print(f"\n Growth share: {growth_share:.2%}")
    except Exception as e:
        print(f"Error occured: {e}")

if __name__ == "__main__":
    main()
