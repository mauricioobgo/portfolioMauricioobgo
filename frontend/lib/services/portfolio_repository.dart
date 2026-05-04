import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/portfolio_content.dart';

abstract class PortfolioRepository {
  Future<PortfolioContent> load();
}

class AssetPortfolioRepository implements PortfolioRepository {
  const AssetPortfolioRepository({
    this.assetPath = 'assets/data/portfolio_content.json',
  });

  final String assetPath;

  @override
  Future<PortfolioContent> load() async {
    final payload = await rootBundle.loadString(assetPath);
    final json = jsonDecode(payload) as Map<String, dynamic>;
    return PortfolioContent.fromJson(json);
  }
}
