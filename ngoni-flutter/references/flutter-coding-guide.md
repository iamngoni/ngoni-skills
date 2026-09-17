# Flutter coding guide

This guide states the user's rules directly and is portable with the skill. It does not require source code from any other application.

## Architecture and directories

Use clean architecture with feature-based organisation. Views render and dispatch events; BLoCs handle business operations through repository interfaces; concrete repositories coordinate API/local adapters. Keep features independent and put only genuinely shared functionality in `core`.

```text
lib/
  main_development.dart
  main_staging.dart
  main_production.dart
  app.dart
  bootstrap.dart
  providers.dart
  injection.dart
  gen/
  l10n/arb/
  core/
    configs/                  # Colours, constants, environments
    services/                 # Storage, notifications, connectivity
    state/
      connectivity/
        connectivity_bloc.dart
        connectivity_event.dart
        connectivity_state.dart
    models/
      data/application_error.dart
      dto/
      repos/
        abs/
        impl/
    utils/                    # Extensions, interceptors, error mapping
    views/widgets/            # Shared controls and feedback components
  commitments/
    models/
      data/commitment.dart
      dto/create_commitment_dto.dart
      repos/
        abs/commitment_repository.dart
        impl/dio_commitment_repository.dart
    state/
      commitments/
        commitments_bloc.dart
        commitments_event.dart
        commitments_state.dart
    views/
      pages/commitments_page.dart
      widgets/commitment_card.dart
```

Every BLoC has its own named state folder, including the only BLoC in a feature. Do not flatten it. Add DTOs and adapters when the feature needs them; avoid empty abstraction layers.

## BLoC and generated states

Never use Cubit. Use BLoC even for a small business state machine. Events describe user/system actions. Handlers await repository operations, emit loading/success/error states and handle both sides of Either. Constructors receive repository interfaces; dispatch with `context.read<CommitmentsBloc>().add(...)`.

Use Freezed unions for events and states. Use public generated event variants when registering typed handlers; let Freezed provide equality and copyWith. Keep the event/state files as parts of the BLoC library, with a single generated Freezed part for that library:

`state/commitments/commitments_bloc.dart`:

```dart
import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part 'commitments_event.dart';
part 'commitments_state.dart';
part 'commitments_bloc.freezed.dart';

class CommitmentsBloc extends Bloc<CommitmentsEvent, CommitmentsState> {
  CommitmentsBloc() : super(const CommitmentsState.initial()) {
    on<CommitmentsResetEvent>((event, emit) {
      emit(const CommitmentsState.initial());
    });
  }
}
```

`state/commitments/commitments_event.dart`:

```dart
part of 'commitments_bloc.dart';

@freezed
sealed class CommitmentsEvent with _$CommitmentsEvent {
  const factory CommitmentsEvent.reset() = CommitmentsResetEvent;
}
```

`state/commitments/commitments_state.dart`:

```dart
part of 'commitments_bloc.dart';

@freezed
sealed class CommitmentsState with _$CommitmentsState {
  const factory CommitmentsState.initial() = CommitmentsInitialState;
  const factory CommitmentsState.loading() = CommitmentsLoadingState;
  const factory CommitmentsState.loaded({required int count}) =
      CommitmentsLoadedState;
  const factory CommitmentsState.error({required String message}) =
      CommitmentsErrorState;
}
```

This compact example shows the file/generation contract. For actual loading/saving, inject the feature repository and implement handlers; a reset-only example is not a complete feature. Do not add JSON generation to transient events/states unless they need persistence or transmission.

Use BlocBuilder for rendering, BlocListener for navigation/toasts, and BlocConsumer when both are needed. Provide application-wide BLoCs in `providers.dart`; scope feature BLoCs to their owning page/flow. Avoid issuing side effects from builders. Await async folds/callbacks; specify concurrency for operations that can overlap. Separate sequential handlers do not establish ordering across all event types.

## Freezed models and json_serializable

Use Freezed data classes and request DTOs with generated JSON conversion. No handwritten equality, copyWith or JSON map implementations. Implement JsonConverter only for wire types that require an explicit conversion.

`models/data/commitment.dart`:

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'commitment.freezed.dart';
part 'commitment.g.dart';

@freezed
abstract class Commitment with _$Commitment {
  const factory Commitment({
    required String id,
    required String title,
    required int amountCents,
    String? notes,
  }) = _Commitment;

  factory Commitment.fromJson(Map<String, dynamic> json) =>
      _$CommitmentFromJson(json);
}
```

Use `@JsonKey` for wire-name mappings and `@Default` for intentional defaults. Define required/nullable fields deliberately; validate domain input before submission. A DTO is a separate Freezed class with a `*DTO` name when API request shape differs from the entity.

Copy [build.yaml](../assets/build.yaml) to configure nested JSON conversion and omission of null values:

```yaml
targets:
  $default:
    builders:
      json_serializable:
        options:
          include_if_null: false
          explicit_to_json: true
```

Preserve the distinction between an omitted field and an explicitly null field in APIs: override `includeIfNull` on fields that must transmit null, rather than replacing generated serialization. Test round trips, nullable copyWith clearing, nested payloads and malformed boundary values where relevant.

Run `dart run build_runner build --delete-conflicting-outputs` after changing annotated inputs. Use watch mode during development when useful. Never edit `.freezed.dart`, `.g.dart`, `injection.config.dart` or generated asset/localisation files manually.

## Dependency injection, repositories and services

Use GetIt with Injectable. Set `preferRelativeImports: true` in `@InjectableInit`. Register BLoCs with `@injectable`; bind repository implementations with `@LazySingleton(as: CommitmentRepository)`. Most services are lazy singletons; use eager singletons only when startup requires them. Use `@module` for third-party dependencies and `@preResolve` for async construction.

Bootstrap initialises Flutter bindings, configures dependencies, awaits required readiness, then runs the app. Resolve GetIt in providers/composition and inject dependencies into business logic rather than locating them inside handlers.

Repository contracts use `Future<Either<ApplicationError, T>>`. Use Dio implementations with configured base URL/timeouts/interceptors. Map DioException to a typed ApplicationError; BLoCs fold failure/success into UI state. Catch unexpected errors with stack traces and report them through configured diagnostics. Keep technical diagnostics separate from actionable user messages. Do not silently turn errors into empty success data.

Wrap ordinary preferences and secure token storage in separate injected services. Store credentials in secure storage. Persist required local changes before announcing success; keep pending remote sync distinct from confirmed persistence. Retries must respect the operation's idempotency and expose retry state to the UI.

## Naming, imports and class organisation

Use snake_case files, PascalCase types, camelCase variables/constants/enum values. Use suffixes `Bloc`, `Event`, `State`, `DTO`, `Repository`, `Service` and `Page`; HTTP repository implementations use `Dio*Repository`.

Group imports in order: Dart SDK, Flutter SDK, external packages, relative project imports. Use relative imports for same-package `lib` files, package imports for external packages and test-to-app imports. Keep exports and `part` declarations consistent with the generator.

Order handwritten class members: static constants, final fields, mutable fields, constructors, factories, getters/setters, public methods, private non-widget methods, overrides. Prefer final values, explicit return types, const constructors and trailing commas. Use required named parameters for mandatory inputs and put `super.key` last. Generated class order is generator-owned.

Add the project header to new authored Dart files: project name, filename, creator and actual creation date, plus the project's established copyright owner/year/website. Preserve existing attribution. Fill it from the target project's identity; do not copy a different app name, owner or historical date. Generated files keep their generator's header. Document public contracts and non-obvious decisions, not obvious statements.

## Widgets, shared controls and responsiveness

One public widget class per file; widget class names cannot start with an underscore. A StatefulWidget and its companion State may share a file, and the State class name may be private. All fields/getters/helpers on widgets and State companions are public. This rule does not expose repository/service/BLoC internals.

Prefer StatelessWidget and extract meaningful sections into their own named widgets. Avoid a large collection of private build helpers. Use BLoC for business state; owned ValueNotifiers/controllers handle transient UI concerns without `setState`. Dispose controllers, notifiers, streams and listeners in the owner.

Reuse shared buttons, outlined buttons, text/password/phone/OTP fields, date/time pickers, loaders, and offline/error components. Use central AppColors, typography and an 8-point spacing scale (8, 16, 24, 32, 48). Keep responsive sizing consistent through shared primitives; use RelativeBuilder with `sx`/`sy` when applying relative_scale. Preserve dynamic type and keyboard/safe-area behavior rather than clamping accessibility text sizes.

## UX rules

- Never leave loading blank. Use contextual progress or skeletons, preserve useful loaded content during refresh, and avoid flicker.
- Acknowledge actions immediately. Prevent duplicate submissions while pending. Explain success and offer a useful retry on recoverable failure.
- Use purposeful motion: approximately 150–200ms for micro-interactions, 250–350ms for content transitions, and 400–600ms for more complex expansion. Centralise timings/easing and respect reduced motion. Do not delay critical actions merely to meet an animation duration.
- Use the design system rather than one-off colours, inline text styles or arbitrary spacing. Product branding remains a product decision.
- Show real state/counts and contextual actions. Keep messages plain and actionable, without exposing technical errors or disguising actual failures.
- Use ARB localisations for visible copy. Provide useful empty states with a next action, and cover slow/offline/interrupted flows.
- Provide semantics, sufficient contrast, keyboard access, dynamic type and platform-appropriate touch targets. Test small/large displays and assistive technologies for changed flows.
- Use const widgets, lazy loading and efficient assets. Profile slow paths before optimising; avoid unnecessary whole-tree rebuilds.

## Lints and verification

The complete reusable lint configuration lives inline in [SKILL.md](../SKILL.md#reusable-lint-configuration), with an identical [analysis_options.yaml](../assets/analysis_options.yaml) asset. Copy the supplied configuration, including its explicit overrides. Check that the installed Very Good Analysis package contains the named included preset. The DCM section requires its own compatible tool; do not claim those checks run just because the YAML parses.

The class order above places fields before constructors. If the included preset enables `sort_constructors_first`, set that rule to false as a deliberate project override so it matches the stated class order. This is separate from the preserved copy of the user's lint file.

Format authored changes, generate code, run `flutter analyze`, and run meaningful BLoC/repository/serialization/widget tests. Use `bloc_test` with mocked boundaries while exercising real BLoC behavior; parser tests must call production parsing rather than merely assert a stub returns itself. Test retries, failures, nullable values and important transitions. Add or update ARBs and run `flutter gen-l10n` when copy changes.

Use the actual environment entrypoint/native flavor and configured scripts for platform checks. Test relevant live/device behavior when claiming it works. A passing generator, analyzer or unit suite does not prove a backend, push-delivery flow or physical device. Report exactly which checks ran.
