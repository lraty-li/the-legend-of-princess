Ext.Osiris.RegisterListener("StatusApplied", 4, "after", function(guid, name, _, _)
    if name == "SNEAKING" then
        AddSpell(guid, "Teleport_ALL", 1, 1)
        AddSpell(guid, "Teleport_LRATY", 1, 1)
        AddSpell(guid, "Teleport_IKO", 1, 1)
        AddSpell(guid, "Teleport_HALL", 1, 1)
        AddSpell(guid, "Teleport_GGBOND", 1, 1)
        AddSpell(guid, "Teleport_Withers", 1, 1)
        AddSpell(guid, "Teleport_Withers_Wardrobe", 1, 1)
    end
end)

-- Ext.Entity.Get(booky).GetComponent(Ext.Entity.Get(booky),"DisplayName").Name="this is book :)"

Ext.Osiris.RegisterListener("AttackedBy", 7, "after", function(defender, attackerOwner, attacker2, damageType, damageAmount, damageCause, storyActionID)
    _P('AttackedBy')
    _D(defender)
end)

Ext.Osiris.RegisterListener("UsingSPell", 5, "before", function(caster, spell, _, _, _)
    if spell == "Teleport_ALL" then
        local party = Osi.DB_Players:Get(nil)
        local counter = 0
        for _, k in pairs(party) do
            _P(k[1])
            TeleportTo(k[1], caster)
            counter = counter + 1
        end
    end
    if spell == "Teleport_LRATY" then
        TeleportTo(caster, 'Humans_Male_Player_Dev_326891bf-1470-b9d7-2ca0-4978c5bf61b7')
    end

    if spell == "Teleport_IKO" then
        TeleportTo(caster, 'Elves_Female_High_Player_9eb1e719-b5b1-98cf-80e3-eabb7b0b6b0c')
    end
    
    if spell == "Teleport_HALL" then
        TeleportTo(caster, 'Humans_Male_Player_Dev_79811c21-8f7c-14ea-9174-519317f939c5')
    end
    
    if spell == "Teleport_GGBOND" then
        TeleportTo(caster, 'HalfOrcs_Male_Player_a7c29645-4168-b4b6-c458-183d09f55a9a')
    end

    if spell == "Teleport_Withers" then
        TeleportTo(caster, '0133f2ad-e121-4590-b5f0-a79413919805')
    end
    
    if spell == "Teleport_Withers_Wardrobe" then 
        -- TeleportTo(caster, 'd94c7491-0868-4444-b83c-82f5454d4b64')
        TeleportTo(caster, 'FUR_GEN_Wardrobe_Player_A_e34b9650-1873-65a3-40cd-a178e71bd756')
        _P('TP wardrobe')
    end
end)
