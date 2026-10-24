local DIR = "edge_addons/fenris_dont_expand_there/"
local ICON = DIR .. "icon.tga"
local PREVIEW = DIR .. "icon_preview.tga"

local function definition(overrides)
	local d = {
		action = "ACTION_TRACK_EDGE_DECORATION_TOOL",
		resName = DIR .. "street.edge",
		icon = { icon = ICON },
		previewIcon = { icon = PREVIEW },
	}
	for k, v in pairs(overrides or {}) do
		d[k] = v
	end
	return d
end

describe("era_icons", function()
	local util, year, input

	-- Passes d through the wrapped forEachDefinition and returns what reaches the callback.
	local function run(d)
		input = d
		local out
		util.forEachDefinition(function(def) out = def end, {})
		return out
	end

	before_each(function()
		tf3.reset()
		year = 2000
		_G.api = { engine = { util = { getYear = function() return year end } } }
		_G.log = { message = spy.new(function() end), warning = spy.new(function() end) }
		util = {
			forEachDefinition = function(fn, _)
				fn(input)
			end,
		}
		tf3.fake("::/gui/construction/construction_react_util.tl", util)
		tf3.require("gui/fenris_dont_expand_there/era_icons.script").doReplace({})
	end)

	it("logs that era icons are enabled", function()
		assert.spy(log.message).was_called_with("fenris_dont_expand_there: era icons enabled")
	end)

	it("switches the add-on icon from the old variant to the modern one at 1940", function()
		local d = run(definition())
		assert.same({ yearFrom = { { 0, DIR .. "icon_old.tga" }, { 1940, ICON } } }, d.icon)
	end)

	it("keeps the modern preview from 1940 on", function()
		year = 1940
		assert.same({ icon = PREVIEW }, run(definition()).previewIcon)
	end)

	it("uses the old preview before 1940", function()
		year = 1939
		assert.same({ icon = DIR .. "icon_old_preview.tga" }, run(definition()).previewIcon)
	end)

	it("leaves other edge decorations alone", function()
		local d = run(definition({ resName = "edge_addons/noise_barrier.edge" }))
		assert.same({ icon = ICON }, d.icon)
	end)

	it("leaves other actions alone", function()
		local d = run(definition({ action = "ACTION_BUILD_STREET" }))
		assert.same({ icon = ICON }, d.icon)
	end)

	it("leaves definitions without a resName or icon alone", function()
		assert.is_nil(run(definition({ resName = false })).icon.yearFrom)
		assert.is_false(run(definition({ icon = false })).icon)
	end)

	it("leaves icons that aren't named icon.tga alone", function()
		local d = run(definition({ icon = { icon = DIR .. "other.tga" } }))
		assert.same({ icon = DIR .. "other.tga" }, d.icon)
	end)

	it("keeps the preview when it has no old variant", function()
		year = 1900
		local d = run(definition({ previewIcon = false }))
		assert.is_false(d.previewIcon)
		assert.equal(DIR .. "icon_old.tga", d.icon.yearFrom[1][2])
	end)
end)

describe("era_icons without forEachDefinition", function()
	it("warns and leaves the game's code untouched", function()
		tf3.reset()
		_G.log = { message = spy.new(function() end), warning = spy.new(function() end) }
		local util = {}
		tf3.fake("::/gui/construction/construction_react_util.tl", util)
		tf3.require("gui/fenris_dont_expand_there/era_icons.script").doReplace({})
		assert.spy(log.warning).was_called(1)
		assert.spy(log.message).was_not_called()
		assert.is_nil(util.forEachDefinition)
	end)
end)
