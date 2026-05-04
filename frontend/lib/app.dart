import 'package:flutter/material.dart';

import 'screens/portfolio_home_page.dart';
import 'services/portfolio_repository.dart';
import 'theme/app_theme.dart';

class PortfolioApp extends StatelessWidget {
  const PortfolioApp({
    super.key,
    PortfolioRepository? repository,
  }) : repository = repository ?? const AssetPortfolioRepository();

  final PortfolioRepository repository;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mauricio Obando',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: PortfolioHomePage(repository: repository),
    );
  }
}
