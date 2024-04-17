# ER図

## tweetデータベース

```mermaid
---
title: "oakbot.db"
---
erDiagram
    input_tera_type_and_name            ||--o| raidInfo                 : ""
    raidInfo                            ||--o| pokemonInfo              : ""
    raidInfo                            ||--|| raidInfo_pokemonAbilities: ""
    raidInfo_pokemonAbilities           ||--|| pokemonAbilities         : ""
    pokemonInfo                         ||--|| pokemonInfo_pokemonAbilities: ""
    pokemonInfo_pokemonAbilities        ||--|| pokemonAbilities         : ""
    raidInfo                            ||--|| pokemonTypes             : ""
    raidInfo                            ||--|| raidInfo_pokemonWeapons  : ""
    raidInfo_pokemonWeapons             ||--|| pokemonWeapons           : ""

    raidInfo {
        int    id                       PK    "ID"
        string name                     FK    "名前"
        string tera_type                FK    "テラスタイプ"
        int    difficulty                     "難易度"
    }

    pokemonInfo {
        int    pokemon_id               PK    "ID"
        string name                     PK    "名前"
        string type1                    FK    "タイプ1"
        string type2                    FK    "タイプ2"
        string ability                        "特性"
        string hidden_ability                 "隠れ特性"
        string base_stats                     "種族値"
    }

    pokemonTypes {
        int     id                      PK    "ID"
        varchar name                          "タイプ"
        string  super_effective_type           "攻撃するとき効果抜群とれるタイプ"
        string  not_very_effective_type        "攻撃するとき効果はいまひとつになるタイプ"
        string  doesnt_affect_type             "攻撃するとき効果がないタイプ"
    }

    pokemonAbilities {
        int     id                      PK    "ID"
        varchar name                          "特性名"
        string  description                   "特性の詳細"
    }

    pokemonWeapons {
        int     id                      PK    "ID"
        varchar name                          "技名"
        string  description                   "技の詳細"
    }

    raidInfo_pokemonAbilities{
        int id                PK "ID"
        int raid_id           FK "raidID"
        int ability_id        FK "abilityID"
    }

    pokemonInfo_pokemonAbilities{
        int id                PK "ID"
        int pokemon_id        FK "pokemonID"
        int ability_id        FK "abilityID"
        int hidden_ability_id FK "abilityID"
    }

    raidInfo_pokemonWeapons{
        int id                  PK "ID"
        int raid_id             FK "raidID"
        int weapon_id           FK "weaponID"
        int limited_weapons_id  FK "weaponID"
    }
```