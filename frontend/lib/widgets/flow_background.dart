import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

class FlowBackground extends StatelessWidget {
  const FlowBackground({super.key});

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  AppPalette.background,
                  AppPalette.backgroundAlt,
                  Color(0xFF06131C),
                ],
              ),
            ),
          ),
          const Positioned.fill(child: CustomPaint(painter: _GridPainter())),
          Positioned(
            top: -120,
            left: -80,
            child: _GlowOrb(
              size: 300,
              color: AppPalette.primary.withValues(alpha: 0.16),
            ),
          ),
          Positioned(
            top: 240,
            right: -120,
            child: _GlowOrb(
              size: 360,
              color: AppPalette.cyan.withValues(alpha: 0.18),
            ),
          ),
          Positioned(
            bottom: -120,
            left: 120,
            child: _GlowOrb(
              size: 260,
              color: AppPalette.warning.withValues(alpha: 0.09),
            ),
          ),
        ],
      ),
    );
  }
}

class _GlowOrb extends StatelessWidget {
  const _GlowOrb({
    required this.size,
    required this.color,
  });

  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: RadialGradient(
          colors: [
            color,
            color.withValues(alpha: 0.0),
          ],
        ),
      ),
    );
  }
}

class _GridPainter extends CustomPainter {
  const _GridPainter();

  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = AppPalette.border.withValues(alpha: 0.14)
      ..strokeWidth = 1;
    const step = 34.0;

    for (double x = 0; x <= size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    for (double y = 0; y <= size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    final tracePaint = Paint()
      ..color = AppPalette.primary.withValues(alpha: 0.22)
      ..strokeWidth = 1.6
      ..style = PaintingStyle.stroke;
    final accentPaint = Paint()
      ..color = AppPalette.cyan.withValues(alpha: 0.18)
      ..strokeWidth = 1.2
      ..style = PaintingStyle.stroke;

    final tracePath = Path()
      ..moveTo(size.width * 0.06, size.height * 0.18)
      ..cubicTo(
        size.width * 0.18,
        size.height * 0.08,
        size.width * 0.30,
        size.height * 0.26,
        size.width * 0.44,
        size.height * 0.18,
      )
      ..cubicTo(
        size.width * 0.58,
        size.height * 0.12,
        size.width * 0.66,
        size.height * 0.26,
        size.width * 0.82,
        size.height * 0.22,
      );
    canvas.drawPath(tracePath, tracePaint);

    final lowerTrace = Path()
      ..moveTo(size.width * 0.14, size.height * 0.72)
      ..cubicTo(
        size.width * 0.22,
        size.height * 0.62,
        size.width * 0.38,
        size.height * 0.78,
        size.width * 0.54,
        size.height * 0.70,
      )
      ..cubicTo(
        size.width * 0.66,
        size.height * 0.64,
        size.width * 0.76,
        size.height * 0.86,
        size.width * 0.92,
        size.height * 0.78,
      );
    canvas.drawPath(lowerTrace, accentPaint);

    final nodePaint = Paint()
      ..color = AppPalette.primary.withValues(alpha: 0.75);
    final accentNodePaint = Paint()
      ..color = AppPalette.cyan.withValues(alpha: 0.72);
    final nodeOffsets = [
      Offset(size.width * 0.12, size.height * 0.14),
      Offset(size.width * 0.44, size.height * 0.18),
      Offset(size.width * 0.82, size.height * 0.22),
      Offset(size.width * 0.20, size.height * 0.68),
      Offset(size.width * 0.54, size.height * 0.70),
      Offset(size.width * 0.86, size.height * 0.80),
    ];

    for (int index = 0; index < nodeOffsets.length; index++) {
      final offset = nodeOffsets[index];
      canvas.drawCircle(
        offset,
        3 + math.min(index.toDouble(), 2),
        index.isEven ? nodePaint : accentNodePaint,
      );
      canvas.drawCircle(
        offset,
        10,
        Paint()
          ..color = (index.isEven ? AppPalette.primary : AppPalette.cyan)
              .withValues(alpha: 0.08)
          ..style = PaintingStyle.fill,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
