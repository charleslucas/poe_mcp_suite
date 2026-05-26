# poe_mcp_suite — All Tools, By Category

A unified index of every MCP tool exposed by the suite. The suite bundles **three Claude-facing MCP servers**:

| Server | Prefix | Tools | Detailed doc |
|--------|--------|------:|--------------|
| **pob-mcp** | `mcp__pob__` | 115 | [pob-mcp/docs/TOOLS.md](pob-mcp/docs/TOOLS.md) |
| **poe-mcp-server** | `mcp__poe__` | 31 | [poe-mcp-server/TOOLS.md](poe-mcp-server/TOOLS.md) |
| **POEMCP** | `mcp__poemcp__` | 13 | [POEMCP/TOOLS.md](POEMCP/TOOLS.md) |
| **Total** | — | **~159** | — |

PathOfBuilding's [`src/API/TOOLS.md`](PathOfBuilding/src/API/TOOLS.md) documents the *Lua-side* actions that pob-mcp wraps. Those are not Claude-callable directly — they're the underlying API.

Tools below are listed **by what they do**, regardless of which server hosts them. Look up specific descriptions in the per-server docs linked above.

---

## 🔧 Build File Management

Loading, saving, snapshotting, and exporting Path of Building build files.

| Tool | Server |
|------|--------|
| `list_builds` | pob |
| `analyze_build` | pob |
| `compare_builds` | pob |
| `get_build_stats` | pob |
| `get_build_notes` / `set_build_notes` | pob |
| `get_build_issues` | pob |
| `export_build` / `export_build_summary` | pob |
| `save_tree` | pob |
| `snapshot_build` / `list_snapshots` / `restore_snapshot` | pob |
| `start_watching` / `stop_watching` / `watch_status` / `get_recent_changes` | pob |

## 👤 Character Import

| Tool | Server |
|------|--------|
| `lua_import_character` | pob |
| `lua_list_characters` | pob |
| `lua_import_pobb` / `lua_share_pobb` | pob |
| `get_character` / `get_character_pob` | poe |

## 🔌 Live PoB Connection (Lua Bridge)

Connecting to a running PoB GUI in TCP mode, or spawning headless LuaJIT.

| Tool | Server |
|------|--------|
| `lua_start` / `lua_stop` | pob |
| `lua_load_build` / `lua_new_build` / `lua_close_build` | pob |
| `lua_save_build` / `lua_reload_build` | pob |
| `lua_get_build_info` | pob |

## 📊 Calculated Stats & Configuration

| Tool | Server |
|------|--------|
| `lua_get_stats` | pob |
| `get_config` / `set_config` | pob |
| `set_enemy_stats` | pob |
| `set_character_level` | pob |
| `save_config_preset` / `load_config_preset` / `list_config_presets` | pob |
| `validate_build` | pob |
| `check_boss_readiness` | pob |
| `analyze_defenses` | pob |

## 🌳 Passive Tree — Data & Allocation

| Tool | Server |
|------|--------|
| `lua_get_tree` / `lua_set_tree` | pob |
| `update_tree_delta` | pob |
| `get_tree_node` | pob ⭐ new |
| `search_tree_nodes` | pob |
| `get_nearby_nodes` | pob |
| `find_path_to_node` | pob |
| `plan_tree_paths` | pob |
| `compare_trees` | pob |
| `refresh_tree_data` | pob |
| `optimize_tree` / `suggest_optimal_nodes` / `get_passive_upgrades` | pob |
| `suggest_masteries` | pob |
| `search_passive` / `get_passive_detail` | poemcp |

## 🌳 Passive Tree — Patches Overlay

For correcting GGG export staleness when it shows up; see [`reference_data/skilltree/PATCHES.md`](reference_data/skilltree/PATCHES.md) (inside the fork submodule) for the protocol.

| Tool | Server |
|------|--------|
| `get_tree_node_patch` | pob ⭐ new |
| `list_tree_patches` | pob ⭐ new |
| `report_tree_node_discrepancy` | pob ⭐ new |

## 🗺 Atlas Tree

Read-only access to atlas tree data via `reference_data/atlastree/` (our fork of GGG's atlas-export). Minimal parity — atlas allocation isn't API-visible, so no "from build frontier" pathing; atlas has no jewel-affects-nodes mechanic, so no jewel-awareness analogs.

| Tool | Server | Notes |
|------|--------|-------|
| `get_atlas_node` | pob ⭐ new | Single-node lookup; supports default/league/ruthless variants |
| `search_atlas_nodes` | pob ⭐ new | Keyword + node-type search across atlas nodes |
| `find_atlas_path_to_node` | pob ⭐ new | BFS shortest path between two atlas nodes (requires explicit `from_node_id`) |

---

## 💎 Passive Tree — Jewel Awareness

Comprehensive coverage of how socketed jewels affect the tree. All new this iteration.

| Tool | Server | Category |
|------|--------|----------|
| `find_jewel_affected_nodes` | pob ⭐ new | Timeless: identifies affected nodes |
| `get_tree_node_with_timeless_jewels` | pob ⭐ new | Timeless: returns transformed stats |
| `evaluate_threshold_jewels` | pob ⭐ new | Brawn / Lethal Assault / etc. trigger checks |
| `list_cluster_jewel_nodes` | pob ⭐ new | Large/Medium/Small cluster summaries |
| `list_radius_effect_jewels` | pob ⭐ new | Energy From Within / Healthy Mind / Might of the Meek / etc. |

## 🪙 Cluster Jewels (specialized)

| Tool | Server |
|------|--------|
| `search_cluster_jewels` | pob |
| `analyze_build_cluster_jewels` | pob |

## 👁 Specs & Item Sets

| Tool | Server |
|------|--------|
| `list_specs` / `select_spec` / `create_spec` / `delete_spec` / `rename_spec` | pob |
| `list_item_sets` / `select_item_set` | pob |

## ⚔️ Gems & Skill Links

| Tool | Server |
|------|--------|
| `add_gem` / `remove_gem` / `toggle_gem` | pob |
| `set_gem_level` / `set_gem_quality` / `validate_gem_quality` | pob |
| `create_socket_group` / `toggle_socket_group` / `setup_skill_with_gems` | pob |
| `remove_skill` / `set_main_skill` / `get_skill_setup` | pob |
| `analyze_skill_links` / `optimize_skill_links` / `find_optimal_links` | pob |
| `suggest_support_gems` / `compare_gem_setups` / `gem_upgrade_path` | pob |
| `search_gem` / `get_gem_detail` | poemcp |

## 🛡 Items, Flasks, Anointments

| Tool | Server |
|------|--------|
| `add_item` / `add_multiple_items` | pob |
| `get_equipped_items` | pob |
| `toggle_flask` | pob |
| `analyze_items` | pob |
| `find_item_upgrades` | pob |
| `find_best_anointment` | pob |
| `suggest_watchers_eye` | pob |
| `suggest_crafting` | pob |
| `search_crafting_mods` | pob ⭐ new |
| `search_item` / `get_item_detail` | poemcp |
| `search_mods` | poemcp |

## 🛒 Trade Search & Pricing

| Tool | Server |
|------|--------|
| `search_trade_items` | pob |
| `find_weighted_trade_items` | pob |
| `compare_trade_items` | pob |
| `get_item_price` | pob |
| `get_leagues` | pob |
| `search_stats` | pob |
| `search_trade` / `search_by_item_mods` | poe |
| `fetch_listing` | poe |
| `price_item` / `price_items` / `price_tab` | poe |
| `get_stat_ids` / `get_filter_info` | poe |
| `price_check` | poemcp |

## 💰 Economy & Currency

| Tool | Server |
|------|--------|
| `get_currency_rates` | pob |
| `find_arbitrage` / `calculate_trading_profit` | pob |
| `ninja_lookup` | poe |
| `currency_overview` | poemcp |

## 📜 Stash & Character API

| Tool | Server |
|------|--------|
| `list_tabs` / `get_tab` / `scan_stash_tabs` | poe |
| `score_rare` | poe |
| `poe_auth` / `poe_auth_status` / `kf_check` | poe |
| `cache_status` | poe |

## 🎯 Loot Filter

| Tool | Server |
|------|--------|
| `find_blocks` / `get_block` / `add_block` / `remove_block` / `replace_block` | poe |
| `set_basetype_rule` | poe |

## 📚 Wiki & Reference Lookups

| Tool | Server |
|------|--------|
| `fetch_wiki_page` | poemcp |
| `fetch_reddit_post` | poemcp |
| `fetch_youtube_transcript` / `fetch_youtube_description` | poemcp |
| `parse_pob` | poemcp |
| `env_search` / `env_detail` | poemcp |

## 🛠 Build Goals, Leveling, Shopping

| Tool | Server |
|------|--------|
| `plan_leveling` | pob |
| `create_budget_build` | pob |
| `generate_shopping_list` | pob |

## 📈 Context & Session Management

| Tool | Server |
|------|--------|
| `get_context_usage` | pob |

---

## How tools are named

Claude sees every tool with an `mcp__<server>__<tool>` prefix. For example, `get_tree_node` (in the pob server) appears as `mcp__pob__get_tree_node` in Claude's context. When tools are described in narrative text, the prefix is usually dropped for readability.

## When a new tool ships

The per-server `TOOLS.md` is the source of truth; this file is a cross-server index. When adding or renaming a tool:

1. Update the relevant per-server `TOOLS.md` first.
2. Add the entry here under the right category.
3. Bump the tool count in the summary table above.

The total count is rough — some tools appear in multiple categories where they fit logically.
