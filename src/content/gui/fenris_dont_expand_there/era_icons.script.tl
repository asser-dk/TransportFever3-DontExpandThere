local construction_react_util = ug_require "::/gui/construction/construction_react_util.tl" as ConstructionReactUtil

local ADD_ON = "edge_addons/fenris_dont_expand_there/street.edge"
local ERA_YEAR = 1940

local era_icons = {}

local wrapper : function(function(ConstructionDefinition), ConstructionActionRepository)

local function oldVariant(path : string, name : string) : string
	if type(path) ~= "string" or not path:find(name .. "%.tga$") then
		return nil
	end
	return (path:gsub(name .. "%.tga$", name:gsub("^icon", "icon_old") .. ".tga"))
end

local function withEraIcons(definition : ConstructionDefinition) : ConstructionDefinition
	if definition.action ~= "ACTION_TRACK_EDGE_DECORATION_TOOL"
		or type(definition.resName) ~= "string"
		or not definition.resName:find(ADD_ON, 1, true)
		or not definition.icon then
		return definition
	end
	local icon = definition.icon.icon
	local oldIcon = oldVariant(icon, "icon")
	if not oldIcon then
		return definition
	end
	local changed : {string:any} = {}
	for k, v in pairs(definition as {string:any}) do
		changed[k] = v
	end
	changed.icon = { yearFrom = { { 0, oldIcon }, { ERA_YEAR, icon } } }

	local preview = definition.previewIcon and definition.previewIcon.icon
	local oldPreview = oldVariant(preview, "icon_preview")
	if oldPreview and api.engine.util.getYear() < ERA_YEAR then
		changed.previewIcon = { icon = oldPreview }
	end
	return changed as ConstructionDefinition
end

-- doReplace runs on every game load, and this module's state can outlive a load,
-- so the game's function may already be our wrapper; wrapping it again would chain one layer per load.
function era_icons.doReplace(_ : ReactReplacementApi)
	local current = construction_react_util.forEachDefinition
	if type(current) ~= "function" then
		log.warning("fenris_dont_expand_there: construction_react_util.forEachDefinition not found, era icons disabled")
		return
	end
	if current ~= wrapper then
		local original = current
		wrapper = function(fn : function(ConstructionDefinition), repository : ConstructionActionRepository)
			original(function(definition : ConstructionDefinition)
				fn(withEraIcons(definition))
			end, repository)
		end
		construction_react_util.forEachDefinition = wrapper
	end
	log.message("fenris_dont_expand_there: era icons enabled")
end

return era_icons
