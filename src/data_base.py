import pandas as pd
from modules.postgres import Postgres
from tqdm import tqdm


def dados_mercadolivre() -> pd.DataFrame:
    # Importando DataSet da tabela "ECOMM".ml1_info PostgresSQL
    with Postgres() as db:
        df_ml_info = db.query('''
            SELECT DISTINCT ON (codpro) *
            FROM (SELECT * FROM "ECOMM".ml1_info WHERE status != 'under_review' ORDER BY status ASC) as x
            ORDER BY codpro''')
    df_ml_info = df_ml_info.query('~jogo and ~kit').reset_index(drop=True)
    return df_ml_info


def dados_produtos_siac() -> pd.DataFrame:
    with Postgres() as db:
        df_products_siac = db.query('''
    SELECT 
    produto.codpro,
    produto.produto,
    produto.codfor,
    produto.codgru,
    grupo.grupo,
    produto.codsubgru,
    produto.codsec,
    produto.num_fab,
    produto.num_orig,
    produto.embala,
    produto.fantasia,
    produto.in_lixeira
    FROM "D-1".produto
    INNER JOIN "D-1".grupo
    ON "D-1".produto.codgru = "D-1".grupo.codgru
    WHERE codfor != '04615'
    ''')
    df_products_siac['embala'] = df_products_siac.embala.replace(0, 1)
    return df_products_siac


def dados_estoque_grupo_siac() -> pd.DataFrame:
    with Postgres() as db:
        df_storage_group = db.query(
            'select cd_loja, codpro, estoque from "H-1".prd_loja')
    df_storage_group = df_storage_group.fillna({'estoque': 0})
    df_storage_group = df_storage_group.astype({'estoque': int})
    df_storage_group = df_storage_group.groupby(
        'codpro').agg({'estoque': sum}).reset_index()
    return df_storage_group


def dados_fotos() -> pd.DataFrame:
    # df_photos_products = pd.read_excel('C:/Users/jefer/Documents/Python/dashboard_products/data/photos_by_codpro_2023_05_29.xlsx', dtype=str)
    with Postgres() as db:
        df_photos_products = db.query('select * from "ECOMM".codpro_photos')
    df_photos_products['img_fraga'] = df_photos_products['img_fraga'] != ''
    df_photos_products['img_siac'] = df_photos_products['img_siac'] != ''
    return df_photos_products


def verify_photo(df_photos_products: pd.DataFrame, df1: pd.DataFrame) -> pd.DataFrame:
    df_photos_products['img_fraga'] = df_photos_products['img_fraga'] != ''
    df_photos_products['img_siac'] = df_photos_products['img_siac'] != ''

    for idx in tqdm(df1.index, total=len(df1)):
        codpro = df1.loc[idx, 'codpro']
        photo_fraga = df_photos_products.query(
            f'codpro == "{codpro}"').img_fraga.values[0]
        photo_siac = df_photos_products.query(
            f'codpro == "{codpro}"').img_siac.values[0]

        if photo_fraga:
            df1.loc[idx, 'img_fraga'] = photo_fraga
        elif photo_siac:
            df1.loc[idx, 'img_siac'] = photo_siac
        else:
            df1.loc[idx, 'img_fraga'] = photo_fraga
            df1.loc[idx, 'img_siac'] = photo_siac
    return df1
    # for idx in tqdm(df_merge_products_storage_photos.index, total=len(df_merge_products_storage_photos)): # indice de cada produto.
    #     if df_merge_products_storage_photos.loc[idx, 'IMAGEM_FRAGA_0']:
    #         df1.loc[idx, 'img_fraga'] = True
    #     else:
    #         df1.loc[idx, 'img_fraga'] = False
    #     if df_merge_products_storage_photos.loc[idx, 'IMAGEM_SIAC_0']:
    #         df1.loc[idx, 'img_siac'] = True
    #     else:
    #         df1.loc[idx, 'img_siac'] = False
    # return df1


def get_infos_postgres(
        query: str) -> pd.DataFrame:
    with Postgres() as db:
        return db.query(query)


def purchase_order(list_consulta: list, list_serie: list = None, purchase_order: bool = False,
                   dt_chegou_purchase_order: bool = False, dt_entrance_notes: bool = False) -> pd.DataFrame:

    list_consulta = str(list_consulta).replace('[', '')
    list_consulta = str(list_consulta).replace(']', '')

    list_serie = str(list_serie).replace('[', '')
    list_serie = str(list_serie).replace(']', '')

    if purchase_order:
        return get_infos_postgres(f'''
            select cd_loja, codfor, serie, numnot, codpro
            from "D-1".prod_nfc
            where codpro in ({list_consulta}) and cd_loja = '01' and emissao > current_date - 60
            order by emissao DESC
        ''')
    if dt_chegou_purchase_order:
        return get_infos_postgres(f'''
            select cd_loja, codfor, serie, numnot, emissao, cadastro, dt_chegou
            from "D-1".compra
            where numnot in ({list_consulta}) and serie in ({list_serie}) and cd_loja = '01' and emissao > current_date - 60
            order by emissao DESC
        ''')
    if dt_entrance_notes:
        return get_infos_postgres(f'''
            select codpro, numnot, cd_loja, dt_entr
            from "D-1".prod_pco
            where numnot in ({list_consulta}) and cd_loja ='01' and emissao > current_date - 60
            order by dt_entr DESC
        ''')


def main():
    df_products_siac = dados_produtos_siac()
    df_storage_group = dados_estoque_grupo_siac()
    df_photos_products = dados_fotos()
    df_ml_info = dados_mercadolivre()
    df_merge_products_storage_siac = pd.merge(
        df_products_siac, df_storage_group, on='codpro', how='inner')
    df_merge_products_storage_photos = pd.merge(
        df_merge_products_storage_siac, df_photos_products, left_on='codpro', right_on='codpro', how='left')
    df_merge_products_storage_photos = df_merge_products_storage_photos.fillna(
        {'img_fraga': False, 'img_siac': False})
    # Para as counas "IMAGEM_FRAGA_0" ate "IMAGEM_FRAGA_14", nan para 0.
    # df_merge_products_storage_photos.iloc[:,16:31] = df_merge_products_storage_photos.iloc[:,16:31].fillna(False)
    # Para as counas "IMAGEM_SIAC_0" ate "IMAGEM_SIAC_4", nan para 0.
    # df_merge_products_storage_photos.iloc[:,31:36] = df_merge_products_storage_photos.iloc[:,31:36].fillna(False)
    # -> QTD de SKUs distintos com pedido de compra ou em estoque no grupo.
    # -> QTD SKUs com pedido de compra ou em estoque no grupo, que tem fotos Vs. que não tem fotos.

    df1 = df_merge_products_storage_photos
    # df1 = verify_photo(df_photos_products, df1)

    df_prod_nfc = purchase_order(list(df1.codpro), purchase_order=True)
    df_compra = purchase_order(list_consulta=list(df_prod_nfc.numnot), list_serie=list(
        df_prod_nfc.serie), dt_chegou_purchase_order=True)
    df_compra = pd.merge(df_prod_nfc, df_compra, on=[
                         'cd_loja', 'codfor', 'serie', 'numnot'], how='left', suffixes=['_prod_nfc', '_compra'])
    df_compra = df_compra.sort_values('dt_chegou', ascending=False)
    df_compra = df_compra.drop_duplicates('codpro')

    df4 = pd.merge(df1, df_compra, on=['codpro', 'codfor'], how='left')
    df4['pedido_compra'] = ~df4['emissao'].isna()

    df5 = pd.merge(df4, df_ml_info, on='codpro', how='left')

    df_results = df5.reset_index(drop=True)
    df_results['in_lixeira'] = df_results.in_lixeira == 'S'
    df_results['price'] = round(df_results.price, 2)
    df_results['cd_loja'] = df_results['cd_loja'].fillna(0)
    df_results = df_results.astype(
        {'embala': 'Int32',
            'estoque': 'Int32',
            'img_fraga': bool,
            'img_siac': bool,
            'price': float,
            'storage': 'Int32',
            'exception': bool,
            'jogo': bool,
            'kit': bool})
    df_results.loc[df_results['storage'] == 0, 'status'] = "out_of_storage"
    df_results['bi_ped_comp_and_stock'] =  list(map(lambda x: 1 if x[0]>0 or x[1] else 0, zip(df_results.estoque, df_results.pedido_compra)))

    return df_results


if __name__ == '__main__':
    df = main()
