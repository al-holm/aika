part of 'language_bloc.dart';

class LanguageState extends Equatable {
  final Locale locale;

  LanguageState(this.locale);

  @override
  List<Object> get props => [locale];
}