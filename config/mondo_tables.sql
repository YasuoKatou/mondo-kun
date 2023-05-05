--
-- カテゴリテーブル
--
drop index if exists categories_idx_01;
drop table if exists categories;
create table categories (
    id serial primary key,      -- カテゴリID
    name text not null          -- カテゴリ名
);
create index categories_idx_01 on categories (
    name
);
--
-- 問答テーブル
--
drop index if exists q_and_a_idx_01;
drop index if exists q_and_a_idx_02;
drop table if exists q_and_a;
create table q_and_a (
    category_id integer,        -- カテゴリID
    question text not null,     -- 質問（トレーニングデータ全文）
    answer text not null,       -- 回答（トレーニングデータ全文）
    list_up_key text not null,  -- 第一段の検索キー
    morphological text not null -- 質問の形態素解析の結果
);
create index q_and_a_idx_01 on q_and_a (
    list_up_key
);
create index q_and_a_idx_02 on q_and_a (
    category_id, list_up_key
);
--[EOF]