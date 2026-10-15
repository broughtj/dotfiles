# Reproduces every number quoted next to a Julia code block in {{STEM}}.qmd.
# Run with `just check {{STEM}}` (or `julia {{DIR}}/check-{{STEM}}.jl`). Exits nonzero on a mismatch.
# Keep it dependency-light: stdlib plus whatever the slides themselves `using`.
# If the deck quotes a shared module (e.g. ../code/foo.jl), include it here the same way.

fails = 0
function expect(label, got, want; tol = 1e-6)
    ok = all(abs.(got .- want) .<= tol)
    ok || (global fails += 1)
    println(rpad(label, 40), ok ? "ok    " : "FAIL  ", got, "   (slides: ", want, ")")
end

# One `expect` per number quoted on the slides, in slide order, e.g.
# expect("slide 7: cumsum(cash_flows)", cumsum([100.0, 50.0, -350.0]), [100.0, 150.0, -200.0])

println(fails == 0 ? "\nall checks passed" : "\n$fails check(s) FAILED")
exit(fails == 0 ? 0 : 1)
