local construction_react_util = ug_require "::/gui/construction/construction_react_util.tl" as ConstructionReactUtil

local ADD_ON = "edge_addons/fenris_dont_expand_there/street.edge"
local ERA_YEAR = 1940

local era_icons = {}

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
	definition.icon = { yearFrom = { { 0, oldIcon }, { ERA_YEAR, icon } } }

	local preview = definition.previewIcon and definition.previewIcon.icon
	local oldPreview = oldVariant(preview, "icon_preview")
	if oldPreview and api.engine.util.getYear() < ERA_YEAR then
		definition.previewIcon = { icon = oldPreview }
	end
	return definition
end

function era_icons.doReplace(_ : ReactReplacementApi)
	local original = construction_react_util.forEachDefinition
	if type(original) ~= "function" then
		log.warning("fenris_dont_expand_there: construction_react_util.forEachDefinition not found, era icons disabled")
		return
	end
	construction_react_util.forEachDefinition = function(fn : function(ConstructionDefinition), repository : ConstructionActionRepository)
		original(function(definition : ConstructionDefinition)
			fn(withEraIcons(definition))
		end, repository)
	end
	log.message("fenris_dont_expand_there: era icons enabled")
end

return era_icons
