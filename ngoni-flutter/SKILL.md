---
name: ngoni-flutter
description: Build, extend, or review Flutter code using Ngoni's coding rules. Requires BLoC in named state subfolders, Freezed and json_serializable, injected repositories, public widget members, and the bundled lint configuration.
---

# Ngoni Flutter

These are the user's chosen rules. Apply them directly rather than inferring alternatives from old code. This skill is self-contained: all referenced resources ship in this directory. Do not depend on another application's files or paths.

## Required conventions

- **BLoC only. Never use Cubit**, including for small features. Dispatch events for business operations; use BlocBuilder for rendering and BlocListener for effects.
- **Always use `state/<bloc_name>/`**, even when a feature has only one BLoC. Keep `<bloc_name>_bloc.dart`, `<bloc_name>_event.dart` and `<bloc_name>_state.dart` together inside that named folder. Never put those three directly under `state/`. The same rule applies to shared BLoCs under `core/state/`.
- **Use Freezed for immutable models, DTOs, BLoC events and states. Use json_serializable for JSON conversion.** Do not handwrite equality, copyWith or fromJson/toJson implementations. Use generated unions and generated serializers; events/states need JSON only when persisted or transmitted.
- Organise features into `models/data`, `models/dto`, `models/repos/abs`, `models/repos/impl`, `state/<bloc_name>`, `views/pages` and `views/widgets`. Data flows `Views → BLoCs → abstract repositories → API/local adapters`.
- Use GetIt with Injectable, constructor-injected repository interfaces, Dio for HTTP adapters, and `Future<Either<ApplicationError, T>>` for fallible repository operations. Generate registrations. Resolve dependencies at composition boundaries, not inside business handlers.
- One public widget class per file; no underscore-prefixed widget names or widget/State members. A companion State class may share the widget's file and may itself have a private name. Private members in non-widget code remain allowed. Put `super.key` last.
- Prefer StatelessWidget. Use BLoCs for business state and owned controllers/ValueNotifiers for transient UI state; do not introduce `setState`. Dispose controllers, notifiers and owned subscriptions.
- Use relative imports within `lib`, package imports across packages and from tests into app code. Group SDK, Flutter, external and relative imports. Use explicit return types, const where possible, final values and trailing commas.
- Keep shared colours, typography, spacing, controls, error mapping and services central. Use localisations and deliberate loading, empty, error and retry states. Read the guide for the concrete layout, class order, DI, UX and examples.

Read [the coding guide](references/flutter-coding-guide.md) for implementation details. Copy [analysis_options.yaml](assets/analysis_options.yaml) and [build.yaml](assets/build.yaml) into a project when setting up these conventions; merge an existing build configuration without discarding unrelated builders. Never edit generated output by hand.

Inspect the target's applicable instructions, SDK, pubspec and task scope before editing. Existing nonconforming code is not a reason to generate more of it. Keep changes scoped to the requested work; adopting this skill does not authorise an unrelated whole-app migration. Do not transplant a backend, brand, environment or credential from a different product.

## Reusable lint configuration

The full user configuration is included here and in the matching asset. Preserve these explicit overrides. Select a compatible `very_good_analysis` package containing the included preset rather than silently substituting a different ruleset.

```yaml
include: package:very_good_analysis/analysis_options.6.0.0.yaml

analyzer:
  exclude: [lib/**.freezed.dart, lib/**.g.dart]

  errors:
    invalid_annotation_target: false
    use_build_context_synchronously: false

  language:
    strict-casts: true
    strict-raw-types: true
    strict-inference: true

formatter:
  trailing_commas: preserve

linter:
  rules:
    cancel_subscriptions: true
    close_sinks: true
    avoid_relative_lib_imports: false
    public_member_api_docs: false
    lines_longer_than_80_chars: true
    avoid_dynamic_calls: true
    avoid_type_to_string: true
    always_declare_return_types: true
    always_specify_types: false
    omit_local_variable_types: false
    prefer_relative_imports: true
    always_use_package_imports: false
    avoid_setters_without_getters: false

dart_code_metrics:
  rules:
    always_remove_listener: true
    dispose_fields: true
```

The `dart_code_metrics` section requires a compatible separately configured tool; it does not become enforced merely by running `flutter analyze`. The BLoC-only, folder-layout, Freezed and widget rules above are also direct review requirements; this YAML alone does not enforce them. Do not add an equality-specific state lint that conflicts with Freezed.

## Dependencies and verification

Use compatible versions of `bloc`, `flutter_bloc`, `freezed_annotation`, `json_annotation`, `dartz`, `dio`, `get_it` and `injectable`. Development tools include `build_runner`, `freezed`, `json_serializable`, `injectable_generator`, `very_good_analysis`, `bloc_test`, `mocktail` and the Flutter test SDK. Do not replace Freezed with a handwritten or alternative model framework to avoid generation.

Run code generation when annotated inputs change:

```sh
dart run build_runner build --delete-conflicting-outputs
```

Run formatting, `flutter analyze`, and meaningful tests for the changed BLoC/repository/serialization/UI behavior. Generate localisations when ARB inputs change. Use the actual entrypoint/flavor for platform checks. Report generated-code checks, tests, builds and device/backend verification separately; do not claim unexecuted checks passed.
