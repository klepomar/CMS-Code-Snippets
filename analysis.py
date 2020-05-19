import numpy as np
import pandas as pd

"""
Dataset obsahuje nasledujici promenne:
 'Age' - vek v rocich
 'Fare' - cena jizdenky
 'Name' - jmeno cestujiciho
 'Parch' - # rodicu/deti daneho cloveka na palube
 'PassengerId' - Id
 'Pclass' - Trida, 1 = 1. trida, 2 = 2.trida, 3 = 3.trida
 'Sex' - pohlavi
 'SibSp' - # sourozencu/manzelu daneho cloveka na ppalube
 'Survived' - 0 = Neprezil, 1 = Prezil
 'Embarked' - Pristav, kde se dany clovek nalodil. C = Cherbourg, Q = Queenstown, S = Southampton
 'Cabin' - Cislo kabiny
 'Ticket' - Cislo tiketu
"""



def load_dataset(train_file_path, test_file_path):
    """
    Napiste funkci, ktera nacte soubory se souboru zadanych parametrem a vytvori dva separatni DataFrame. Pro testovani vyuzijte data 'data/train.csv' a 'data/test.csv'
    Ke kazdemu dataframe pridejte sloupecek pojmenovaný jako "Label", ktery bude obsahovat hodnoty "Train" pro train.csv a "Test" pro test.csv.

    1. Pote slucte oba dataframy.
    2. Z vysledneho slouceneho DataFramu odstraňte sloupce  "Ticket", "Embarked", "Cabin".
    3. Sloučený DataDrame bude mít index od 0 do do počtu řádků.
    4. Vratte slouceny DataDrame.
    """
    train_data = pd.read_csv(train_file_path)
    test_data = pd.read_csv(test_file_path)

    train_data['Label'] = 'Train'
    test_data['Label'] = 'Test'
    merged_data = train_data.merge(test_data, how='outer')
    merged_data.info()
    merged_data.drop(["Ticket", "Embarked", "Cabin"], axis=1, inplace=True)

    return merged_data


def get_missing_values(df : pd.DataFrame) -> pd.DataFrame:
    """
    Ze zadaneho dataframu zjistete chybejici hodnoty. Vyvorte DataFrame, ktery bude obsahovat v indexu jednotlive promenne
    a ve prvnim sloupci bude promenna 'Total' obsahujici celkovy pocet chybejicich hodnot a ve druhem sloupci promenna 'Percent',
    ve ktere bude procentualni vyjadreni chybejicich hodnot vuci celkovemu poctu radku v tabulce.
    DataFrame seradte od nejvetsich po nejmensi hodnoty.
    Vrattre DataFrame chybejicich hodnot a celkovy pocet chybejicich hodnot.

    Priklad:

               |  Total  |  Percent
    "Column1"  |   34    |    76
    "Column2"  |   0     |    0

    """

    column = list(df)
    total_missing = df.isnull().sum().sum()
    sum_of_value = df.isnull().sum()
    sum_of_value.values
    percent = list()
    for i in sum_of_value.values:
        percent.append(round(i / total_missing * 100, 2))

    df_new = pd.DataFrame(list(zip(sum_of_value.values, percent)), columns=['Total', 'Percent'], index=column)

    return df_new

def substitute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chybejici hodnoty ve sloupecku "Age" nahradte meanem hodnot z "Age".
    Chybejici hodnoty ve sloupecku "Fare" nahradte meadianem hodnot z "Fare".
    V jednom pripade pouzijte "loc" a ve druhem "fillna".
    Zadany DataFrame neupravujte, ale vytvorte si kopii.
    Vratte upraveny DataFrame.
    """




    new_df = df
    new_df.loc[pd.isnull(new_df.Age), 'Age'] = new_df['Age'].mean()
    new_df['Fare'].fillna(new_df['Fare'].median())

    return new_df



def get_correlation(df: pd.DataFrame) -> float:
    """
    Spocitejte korelaci pro "Age" a "Fare" a vratte korelaci mezi "Age" a "Fare".
    """


    correlation = df['Age'].corr(df['Fare'])

    return correlation
 
def get_survived_per_class(df : pd.DataFrame, group_by_column_name : str) ->pd.DataFrame:
    """
    Spocitejte prumer z promenne "Survived" pro kazdou skupinu zadanou parametrem "group_by_column_name".
    Hodnoty seradte od nejvetsich po mejmensi.
    Hodnoty "Survived" zaokhroulete na 2 desetinna mista.
    Vratte pd.DataFrame.

    Priklad:

    get_survived_per_class(df, "Sex")

                 Survived
    Male     |      0.32
    Female   |      0.82

    """
    names = df[str].unique()
    
    values = list()

    for i in names:
      
        print(i)
        total = df[str].value_counts()[i]
        print(total)
        survived = df.loc[df.Sex == i, 'Survived'].value_counts()[1]
        print(survived)
        percent = round((total / survived) / 100, 2)
        values.append(percent)

        
    new_df = pd.DataFrame(values, index=names, columns=['Survived'])
    print(new_df)

    

def get_outliers(df: pd.DataFrame) -> (int, str):
    """
    Vyfiltrujte odlehle hodnoty (outliers) ve sloupecku "Fare" pomoci metody IRQ.
    Tedy spocitejte rozdil 3. a 1. kvantilu, tj. IQR = Q3 - Q1.
    Pote odfiltrujte vsechny hodnoty nesplnujici: Q1 - 1.5*IQR < "Fare" < Q3 + 1.5*IQR.
    Namalujte box plot pro sloupec "Fare" pred a po vyfiltrovani outlieru.
    Vratte tuple obsahujici pocet outlieru a jmeno cestujiciho pro nejvetsi outlier.
    """

    Q1 = df['Fare'].quantile()
    Q3 = df['Fare'].quantile()
    IQR = Q3 - Q1

    filtered = df.query('(@Q1 - 1.5 * @IQR) <= Fare <= (@Q3 + 1.5 * @IQR)')


    df.boxplot(column='Fare')
    filtered.boxplot(column='Fare')
    #filtered.info()
    count = filtered['Fare'].count()

    return (count, filtered.loc[filtered['Fare'].idxmax()].loc['Name'])


def normalise(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Naskalujte sloupec "col" zadany parametrem pro kazdou "Pclass" hodnotu z dataframu "df" zvlast.
    Pouzijte vzorec: scaled_x_i = (x_i - min(x)) / (max(x) - min(x)), kde "x_i" prestavuje konkretni hodnotu ve sloupeci "col".
    Vratte naskalovany dataframe.
    """

    ### Implementujte sve reseni.


def create_new_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vytvorte 3 nove promenne:
    1. "Fare_scaled" - vytvorte z "Fare" tak, aby mela nulovy prumer a jednotkovou standartni odchylku.
    2. "Age_log" - vytvorte z "Age" tak, aby nova promenna byla logaritmem puvodni "Age".
    3. "Sex" - Sloupec "Sex" nahradte: "female" -> 1, "male" -> 0, kde 0 a 1 jsou integery.

    Nemodifikujte predany DataFrame, ale vytvorte si novy, upravte ho a vratte jej.
    """

    new_df = df
    new_df['Age_log'] = np.log(df['Age'])
    new_df.loc[new_df['Sex'] == 'male', 'Sex'] = 1
    new_df.loc[new_df['Sex'] == 'female', 'Sex'] = 0
    


def determine_survival(df: pd.DataFrame, n_interval: int, age: float, sex: str) -> float:
    """
    Na zaklade statistickeho zpracovani dat zjistete pravdepodobnost preziti Vami zadaneho cloveka (zadava se vek a pohlavi pomoci parametru "age" a "sex")

    Vsechny chybejici hodnoty ve vstupnim DataFramu ve sloupci "Age" nahradte prumerem.
    Rozdelte "Age" do n intervalu zadanych parametrem "n_interval". Napr. pokud bude Age mit hodnoty [2, 13, 18, 25] a mame jej rozdelit do 2 intervalu,
    tak bude vysledek:

    0    (1.977, 13.5]
    1    (1.977, 13.5]
    2     (13.5, 25.0]
    3     (13.5, 25.0]

    Pridejte k rozdeleni jeste pohlavi. Tj. pro kazdou kombinaci pohlavi a intervalu veku zjistete prumernou
    pravdepodobnost preziti ze sloupce "Survival" a tu i vratte.

    Vysledny DataFrame:

    "AgeInterval"   |    "Sex"    |   "Survival Probability"
       (0-10)       | "male"      |            0.21
       (0-10)       | "female"    |            0.28
       (10-20)      | "male"      |            0.10
       (10-20)      | "female"    |            0.15
       atd...

    Takze vystup funkce determine_survival(df, n_interval=20, age = 5, sex = "male") bude 0.21. Tato hodnota bude navratovou hodnotou funkce.

    """

    ### Implementujte sve reseni.