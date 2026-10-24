-- Type of the `t` object passed to in-game test suites (tests/ingame/*.tl). `tf3-test init` copies this
-- file into the mod's repo root; suites import it with `local type Test = require("tf3test")`.
local record Test
	type Phase = function(ctx : {string : any})
	test : function(name : string, fn : Phase | {Phase})
	ok : function(cond : any, msg? : string)
	eq : function(actual : any, expected : any, msg? : string)
	near : function(actual : number, expected : number, tolerance : number, msg? : string)
	log : function(...: any)
end

return Test
