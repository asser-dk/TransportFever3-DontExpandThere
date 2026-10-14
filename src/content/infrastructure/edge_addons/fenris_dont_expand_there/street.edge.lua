function data()
return {
    availability = {
        yearFrom = 0,
        yearTo = 4000,
    },
    cost = {
        price = 100,
        priceScale = 1,
    },
    maintenance = {
        runningCosts = 0,
    },
    desc = {
        icon = "icon.tga",
        previewIcon = "icon_preview.tga",
        name = _("FENRIS_DONT_EXPAND_THERE_NAME"),
        description = _("FENRIS_DONT_EXPAND_THERE_DESCRIPTION"),
    },
    categoryList = {
        categories = {
            "barrier"
        }
    },
    builderAudioRes = "::/gui/construction/sound/tool_edge_noise_barrier.builder_audio",
    order = 2,
    menuCategory = {
        categories = {
            {
                category = "roads_tools",
                order = 450,
            },
        }
    },

    repModel = "empty.mdl",
    length = 3.0,
    stretch = true,
    verticalAlignment = "Shear",
    offset = 0.0,
    snapMode = "Side",
    skipSameInParallelStrip = true,

    incompatibleTags = {"track", "tunnel", "decorated"},

    modifiers = {
        noiseModifier = 0.0,
    },

    preventParcels = true,
}
end
