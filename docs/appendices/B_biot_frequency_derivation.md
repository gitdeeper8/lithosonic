# Appendix B: Biot Critical Frequency Derivation

## Definition

The Biot critical frequency f_c marks the crossover between propagating and diffusive slow-wave behaviour:

```

f_c = η · φ / (2π · κ · ρ_f · α_∞)

```

where:

| Symbol | Parameter | Units |
|--------|-----------|-------|
| η | Fluid dynamic viscosity | Pa·s |
| φ | Porosity | dimensionless |
| κ | Absolute permeability | m² |
| ρ_f | Fluid density | kg/m³ |
| α_∞ | High-frequency tortuosity | dimensionless (≥1) |

## Example Calculations

### Water-saturated sandstone
```

η = 10⁻³ Pa·s
φ = 0.20
κ = 10⁻¹³ m² (100 mD)
ρ_f = 1000 kg/m³
α_∞ = 2.0

f_c = (10⁻³ × 0.20) / (2π × 10⁻¹³ × 1000 × 2.0) ≈ 159 Hz

```

### Tight basement granite
```

κ = 10⁻¹⁸ m² (10⁻³ mD)
f_c ≈ 1.6 × 10⁶ Hz (far above LITHO-SONIC band)

```

## Physical Interpretation

- **f < f_c**: Diffusive regime - slow wave is non-propagating, pressure diffusion
- **f > f_c**: Propagating regime - slow wave propagates with attenuation

This transition from propagating to diffusive behaviour with decreasing permeability is the physical basis for LITHO-SONIC's permeability-sensitive monitoring capability.
