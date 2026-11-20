# Loadout assembly — the part the MCP surface cannot create

`create_loadout` / `copy_loadout` build all four loadout families (tree spec, item set, skill set, config set) under one title. **Jewel sockets** are the exception: they need a small XML edit. Do it while PoB holds the build **only in this order**: save via `lua_save_build`, edit the file, then `lua_reload_build`. Editing before saving loses the in-memory work. Do this only on a build the user agreed to have edited (or a copy).

PoB writes UTF-8 without BOM; write back the same way, or PoB loads a blank level-1 build:

```powershell
[System.IO.File]::WriteAllText($path, $xml, (New-Object System.Text.UTF8Encoding($false)))
```

## Jewel sockets live on the tree spec, not in the item set

```xml
<Tree activeSpec="4">
  <Spec … title="BUDGET">
    <URL>…</URL>
    <Sockets>
      <Socket itemId="53" nodeId="6230"/>
      <Socket itemId="2"  nodeId="7960"/>
    </Sockets>
  </Spec>
</Tree>
```

Each `<Socket itemId=… nodeId=…>` points at an `<Item id=…>` block. To change a jewel, add a new `<Item id="N">` block (unique IDs above the current maximum) and repoint the socket. Only sockets of the **active spec** matter; other specs keep their own list.

An item block is plain item text, tab-indented after the tag:

```xml
<Item id="53">
			Rarity: RARE
Budget Jewel 1
Viridian Jewel
Item Level: 84
Implicits: 0
+18 to maximum Life
+10% to Chaos Resistance
</Item>
```

## After the edit

`lua_reload_build()` → `select_loadout({name:"BUDGET"})` → `get_pob_warnings()`. If a warning appears, it belongs to the budget loadout, not the target — fix it there.
