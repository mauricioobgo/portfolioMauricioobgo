import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/portfolio_content.dart';
import '../services/portfolio_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/flow_background.dart';
import '../widgets/section_shell.dart';

class PortfolioHomePage extends StatefulWidget {
  const PortfolioHomePage({
    super.key,
    required this.repository,
  });

  final PortfolioRepository repository;

  @override
  State<PortfolioHomePage> createState() => _PortfolioHomePageState();
}

class _PortfolioHomePageState extends State<PortfolioHomePage> {
  final ScrollController _scrollController = ScrollController();
  final Map<String, GlobalKey> _sectionKeys = {
    'about': GlobalKey(),
    'experience': GlobalKey(),
    'projects': GlobalKey(),
    'github': GlobalKey(),
    'certifications': GlobalKey(),
    'contact': GlobalKey(),
  };

  late final Future<PortfolioContent> _contentFuture;

  @override
  void initState() {
    super.initState();
    _contentFuture = widget.repository.load();
  }

  Future<void> _scrollTo(String section) async {
    final context = _sectionKeys[section]?.currentContext;
    if (context == null) {
      return;
    }
    await Scrollable.ensureVisible(
      context,
      duration: const Duration(milliseconds: 650),
      curve: Curves.easeInOutCubic,
      alignment: 0.06,
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<PortfolioContent>(
      future: _contentFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Scaffold(
            body: Stack(
              children: [
                Positioned.fill(child: FlowBackground()),
                Center(child: CircularProgressIndicator()),
              ],
            ),
          );
        }

        if (snapshot.hasError || !snapshot.hasData) {
          return Scaffold(
            body: Stack(
              children: [
                const Positioned.fill(child: FlowBackground()),
                Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 560),
                      child: Card(
                        child: Padding(
                          padding: const EdgeInsets.all(28),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Unable to load portfolio content',
                                style: Theme.of(context)
                                    .textTheme
                                    .headlineSmall
                                    ?.copyWith(fontWeight: FontWeight.w700),
                              ),
                              const SizedBox(height: 12),
                              Text(
                                '${snapshot.error}',
                                style: Theme.of(context)
                                    .textTheme
                                    .bodyMedium
                                    ?.copyWith(color: AppPalette.textMuted),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
        }

        final content = snapshot.data!;
        return LayoutBuilder(
          builder: (context, constraints) {
            final isWide = constraints.maxWidth >= 1040;
            return Scaffold(
              body: Stack(
                children: [
                  const Positioned.fill(child: FlowBackground()),
                  SafeArea(
                    child: SelectionArea(
                      child: SingleChildScrollView(
                        controller: _scrollController,
                        padding: EdgeInsets.symmetric(
                          horizontal: isWide ? 28 : 18,
                          vertical: 18,
                        ),
                        child: Center(
                          child: ConstrainedBox(
                            constraints: const BoxConstraints(maxWidth: 1180),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                _TopBar(
                                  compact: !isWide,
                                  onNavigate: _scrollTo,
                                ),
                                SizedBox(height: isWide ? 32 : 24),
                                _HeroPanel(
                                  profile: content.profile,
                                  metadata: content.metadata,
                                  onOpenResume: () => _launchExternal(
                                      content.profile.resumeLink),
                                  onOpenLinkedIn: () => _launchExternal(
                                    content.profile.socialLinks['linkedin'] ??
                                        '',
                                  ),
                                  onOpenGithub: () => _launchExternal(
                                      content.profile.githubUrl),
                                ),
                                const SizedBox(height: 48),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['about']!,
                                  child: SectionShell(
                                    eyebrow: 'SYSTEM / PROFILE',
                                    title:
                                        'Cloud delivery with AI-native execution.',
                                    description:
                                        'The frontend is now a Flutter command center, while Python keeps the weekly and monthly content refresh loop alive behind the scenes.',
                                    child: _AboutSection(
                                      profile: content.profile,
                                      metadata: content.metadata,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 56),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['experience']!,
                                  child: SectionShell(
                                    eyebrow: 'LATEST EXPERIENCE',
                                    title:
                                        'Recent roles, current context, and delivery range.',
                                    description:
                                        'These cards prioritize the latest three experiences and keep the source references visible, so the portfolio reads like a verified professional timeline instead of a static resume dump.',
                                    child: _ExperienceSection(
                                      experience: content.experience,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 56),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['projects']!,
                                  child: SectionShell(
                                    eyebrow: 'FEATURED WORK',
                                    title:
                                        'Selected platform work and data products.',
                                    description:
                                        'The showcase balances high-level delivery narratives with GitHub-backed activity so the page feels credible, current, and closer to a working engineering dashboard.',
                                    child: _ProjectsSection(
                                      projects: content.projects,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 56),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['github']!,
                                  child: SectionShell(
                                    eyebrow: 'GITHUB FEED',
                                    title:
                                        'Weekly-refreshed repository activity.',
                                    description:
                                        'The repository list comes from the Python sync cadence and highlights current coding motion without hardcoding hand-picked repo metadata into the Flutter app.',
                                    child:
                                        _GithubSection(github: content.github),
                                  ),
                                ),
                                const SizedBox(height: 56),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['certifications']!,
                                  child: SectionShell(
                                    eyebrow: 'CERTIFICATIONS',
                                    title:
                                        'LinkedIn-backed learning and AWS professional depth.',
                                    description:
                                        'Certification cards link back to LinkedIn, with the AWS professional and machine learning specialty entries intentionally surfaced as first-class proof points.',
                                    child: _CertificationsSection(
                                      certifications: content.certifications,
                                    ),
                                  ),
                                ),
                                const SizedBox(height: 56),
                                _AnchoredSection(
                                  sectionKey: _sectionKeys['contact']!,
                                  child: SectionShell(
                                    eyebrow: 'CONTACT / LINKS',
                                    title:
                                        'Open to data, AI, and cloud platform work.',
                                    description:
                                        'If you want to review architecture, delivery history, or current GitHub work, this section keeps the direct paths close at hand.',
                                    child: _ContactSection(
                                        profile: content.profile),
                                  ),
                                ),
                                const SizedBox(height: 48),
                                _Footer(metadata: content.metadata),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}

class _TopBar extends StatelessWidget {
  const _TopBar({
    required this.compact,
    required this.onNavigate,
  });

  final bool compact;
  final ValueChanged<String> onNavigate;

  @override
  Widget build(BuildContext context) {
    final navItems = const {
      'about': 'Profile',
      'experience': 'Experience',
      'projects': 'Projects',
      'github': 'GitHub',
      'certifications': 'Certifications',
      'contact': 'Contact',
    };

    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: compact ? 18 : 22,
        vertical: compact ? 16 : 18,
      ),
      decoration: BoxDecoration(
        color: AppPalette.panel.withValues(alpha: 0.72),
        borderRadius: BorderRadius.circular(28),
        border: Border.all(color: AppPalette.border),
      ),
      child: compact
          ? Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const _BrandBlock(),
                const SizedBox(height: 16),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: navItems.entries
                      .map(
                        (entry) => _NavButton(
                          label: entry.value,
                          onTap: () => onNavigate(entry.key),
                        ),
                      )
                      .toList(),
                ),
              ],
            )
          : Row(
              children: [
                const _BrandBlock(),
                const Spacer(),
                Wrap(
                  spacing: 10,
                  children: navItems.entries
                      .map(
                        (entry) => _NavButton(
                          label: entry.value,
                          onTap: () => onNavigate(entry.key),
                        ),
                      )
                      .toList(),
                ),
              ],
            ),
    );
  }
}

class _BrandBlock extends StatelessWidget {
  const _BrandBlock();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'MO / FLOW',
          style: Theme.of(context).textTheme.labelLarge?.copyWith(
                fontFamily: 'IBMPlexMono',
                color: AppPalette.primarySoft,
                letterSpacing: 2.2,
                fontWeight: FontWeight.w600,
              ),
        ),
        const SizedBox(height: 6),
        Text(
          'Mauricio Obando',
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w700,
              ),
        ),
      ],
    );
  }
}

class _HeroPanel extends StatelessWidget {
  const _HeroPanel({
    required this.profile,
    required this.metadata,
    required this.onOpenResume,
    required this.onOpenLinkedIn,
    required this.onOpenGithub,
  });

  final Profile profile;
  final Metadata metadata;
  final VoidCallback onOpenResume;
  final VoidCallback onOpenLinkedIn;
  final VoidCallback onOpenGithub;

  @override
  Widget build(BuildContext context) {
    final isWide = MediaQuery.sizeOf(context).width >= 1040;
    return Container(
      padding: EdgeInsets.all(isWide ? 30 : 22),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            AppPalette.panel.withValues(alpha: 0.94),
            const Color(0xFF0D1D29),
            const Color(0xFF08141D),
          ],
        ),
        borderRadius: BorderRadius.circular(36),
        border: Border.all(color: AppPalette.border),
        boxShadow: [
          BoxShadow(
            color: AppPalette.primary.withValues(alpha: 0.08),
            blurRadius: 50,
            spreadRadius: 4,
          ),
        ],
      ),
      child: isWide
          ? Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  flex: 6,
                  child: _HeroCopy(
                    profile: profile,
                    metadata: metadata,
                    onOpenResume: onOpenResume,
                    onOpenLinkedIn: onOpenLinkedIn,
                    onOpenGithub: onOpenGithub,
                  ),
                ),
                const SizedBox(width: 24),
                Expanded(flex: 5, child: _HeroSystemCard(profile: profile)),
              ],
            )
          : Column(
              children: [
                _HeroCopy(
                  profile: profile,
                  metadata: metadata,
                  onOpenResume: onOpenResume,
                  onOpenLinkedIn: onOpenLinkedIn,
                  onOpenGithub: onOpenGithub,
                ),
                const SizedBox(height: 22),
                _HeroSystemCard(profile: profile),
              ],
            ),
    );
  }
}

class _HeroCopy extends StatelessWidget {
  const _HeroCopy({
    required this.profile,
    required this.metadata,
    required this.onOpenResume,
    required this.onOpenLinkedIn,
    required this.onOpenGithub,
  });

  final Profile profile;
  final Metadata metadata;
  final VoidCallback onOpenResume;
  final VoidCallback onOpenLinkedIn;
  final VoidCallback onOpenGithub;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: [
            const _SignalPill(
                label: 'PYTHON + FLUTTER', accent: AppPalette.primarySoft),
            const _SignalPill(
                label: 'AI CLOUD DELIVERY', accent: AppPalette.cyan),
            _SignalPill(
              label: metadata.refreshScope.isEmpty
                  ? 'SYNC READY'
                  : 'SYNC ${metadata.refreshScope.toUpperCase()}',
              accent: AppPalette.warning,
            ),
          ],
        ),
        const SizedBox(height: 22),
        Text(
          profile.title,
          style: Theme.of(context).textTheme.displaySmall?.copyWith(
                fontWeight: FontWeight.w700,
                height: 0.96,
              ),
        ),
        const SizedBox(height: 14),
        Text(
          profile.subtitle,
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                color: AppPalette.textMuted,
                height: 1.28,
                fontWeight: FontWeight.w500,
              ),
        ),
        const SizedBox(height: 18),
        ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 640),
          child: Text(
            profile.about,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: AppPalette.textMuted,
                  height: 1.7,
                ),
          ),
        ),
        const SizedBox(height: 24),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: profile.skills
              .take(4)
              .map((skill) => Chip(label: Text(skill)))
              .toList(),
        ),
        const SizedBox(height: 26),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            _ActionButton(
              label: 'Resume',
              icon: Icons.picture_as_pdf_outlined,
              onTap: onOpenResume,
            ),
            _ActionButton(
              label: 'LinkedIn',
              icon: Icons.north_east_rounded,
              onTap: onOpenLinkedIn,
              filled: false,
            ),
            _ActionButton(
              label: 'GitHub',
              icon: Icons.code_rounded,
              onTap: onOpenGithub,
              filled: false,
            ),
          ],
        ),
        const SizedBox(height: 28),
        Wrap(
          spacing: 14,
          runSpacing: 14,
          children: [
            _MetricTile(
              label: 'Focus',
              value: 'AI + Data',
              accent: AppPalette.primarySoft,
            ),
            _MetricTile(
              label: 'Repos',
              value: '${profile.githubPublicRepos}+',
              accent: AppPalette.cyan,
            ),
            _MetricTile(
              label: 'Followers',
              value: '${profile.githubFollowers}',
              accent: AppPalette.warning,
            ),
            _MetricTile(
              label: 'Deploy',
              value: 'gh-pages',
              accent: AppPalette.primary,
            ),
          ],
        ),
      ],
    );
  }
}

class _HeroSystemCard extends StatelessWidget {
  const _HeroSystemCard({
    required this.profile,
  });

  final Profile profile;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(22),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(28),
            color: AppPalette.background.withValues(alpha: 0.72),
            border: Border.all(color: AppPalette.border),
          ),
          child: Column(
            children: [
              Row(
                children: [
                  _AvatarBadge(avatarUrl: profile.avatarUrl),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          profile.name,
                          style:
                              Theme.of(context).textTheme.titleLarge?.copyWith(
                                    fontWeight: FontWeight.w700,
                                  ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          [
                            if (profile.company.isNotEmpty) profile.company,
                            if (profile.location.isNotEmpty) profile.location,
                          ].join('  //  '),
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: AppPalette.textMuted,
                                  ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              const _CodeFlowBlock(),
            ],
          ),
        ),
      ],
    );
  }
}

class _AboutSection extends StatelessWidget {
  const _AboutSection({
    required this.profile,
    required this.metadata,
  });

  final Profile profile;
  final Metadata metadata;

  @override
  Widget build(BuildContext context) {
    final isWide = MediaQuery.sizeOf(context).width >= 960;
    final left = _InfoCard(
      title: 'Profile Brief',
      icon: Icons.bolt_rounded,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            profile.bio.isEmpty ? profile.about : profile.bio,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: AppPalette.textMuted,
                  height: 1.7,
                ),
          ),
          const SizedBox(height: 18),
          Wrap(
            spacing: 14,
            runSpacing: 14,
            children: [
              _DataPoint(label: 'Location', value: profile.location),
              _DataPoint(label: 'Company', value: profile.company),
              _DataPoint(
                label: 'Refresh Scope',
                value: metadata.refreshScope.isEmpty
                    ? 'manual'
                    : metadata.refreshScope,
              ),
              _DataPoint(label: 'Frontend', value: metadata.frontend),
            ],
          ),
        ],
      ),
    );

    final right = _InfoCard(
      title: 'Execution Surface',
      icon: Icons.hub_rounded,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'The site runs as a static Flutter web app while Python handles curated YAML, GitHub sync cadence, and content packaging for deployment.',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: AppPalette.textMuted,
                  height: 1.7,
                ),
          ),
          const SizedBox(height: 18),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: const [
              Chip(label: Text('Weekly GitHub refresh')),
              Chip(label: Text('Monthly profile review')),
              Chip(label: Text('Monthly certification review')),
              Chip(label: Text('Static gh-pages deploy')),
            ],
          ),
        ],
      ),
    );

    return isWide
        ? Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: left),
              const SizedBox(width: 18),
              Expanded(child: right),
            ],
          )
        : Column(
            children: [
              left,
              const SizedBox(height: 18),
              right,
            ],
          );
  }
}

class _ExperienceSection extends StatelessWidget {
  const _ExperienceSection({
    required this.experience,
  });

  final List<Experience> experience;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: experience
          .map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: 18),
              child: _ExperienceCard(item: item),
            ),
          )
          .toList(),
    );
  }
}

class _ProjectsSection extends StatelessWidget {
  const _ProjectsSection({
    required this.projects,
  });

  final List<Project> projects;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final cardWidth = width >= 1100
        ? 350.0
        : width >= 760
            ? 320.0
            : double.infinity;

    return Wrap(
      spacing: 18,
      runSpacing: 18,
      children: projects
          .map(
            (project) => SizedBox(
              width: cardWidth,
              child: _ProjectCard(project: project),
            ),
          )
          .toList(),
    );
  }
}

class _GithubSection extends StatelessWidget {
  const _GithubSection({
    required this.github,
  });

  final GithubData github;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final cardWidth = width >= 1100
        ? 350.0
        : width >= 760
            ? 320.0
            : double.infinity;
    final repositories = github.repositories.take(6).toList();

    return Wrap(
      spacing: 18,
      runSpacing: 18,
      children: repositories
          .map(
            (repo) => SizedBox(
              width: cardWidth,
              child: _RepoCard(repo: repo),
            ),
          )
          .toList(),
    );
  }
}

class _CertificationsSection extends StatelessWidget {
  const _CertificationsSection({
    required this.certifications,
  });

  final List<Certification> certifications;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final cardWidth = width >= 1100
        ? 350.0
        : width >= 760
            ? 320.0
            : double.infinity;

    return Wrap(
      spacing: 18,
      runSpacing: 18,
      children: certifications
          .map(
            (certification) => SizedBox(
              width: cardWidth,
              child: _CertificationCard(certification: certification),
            ),
          )
          .toList(),
    );
  }
}

class _ContactSection extends StatelessWidget {
  const _ContactSection({
    required this.profile,
  });

  final Profile profile;

  @override
  Widget build(BuildContext context) {
    final contactCards = [
      _ContactCard(
        title: 'Email',
        value: profile.email,
        caption: 'Direct channel for project work and collaboration.',
        onTap: () => _launchExternal('mailto:${profile.email}'),
      ),
      _ContactCard(
        title: 'LinkedIn',
        value: profile.socialLinks['linkedin'] ?? '',
        caption: 'Work history, certifications, and current public profile.',
        onTap: () => _launchExternal(profile.socialLinks['linkedin'] ?? ''),
      ),
      _ContactCard(
        title: 'GitHub',
        value: profile.githubUrl,
        caption: 'Recent repositories and engineering experiments.',
        onTap: () => _launchExternal(profile.githubUrl),
      ),
    ];

    return Wrap(
      spacing: 18,
      runSpacing: 18,
      children: contactCards
          .map(
            (card) => SizedBox(
              width: MediaQuery.sizeOf(context).width >= 1100
                  ? 350
                  : MediaQuery.sizeOf(context).width >= 760
                      ? 320
                      : double.infinity,
              child: card,
            ),
          )
          .toList(),
    );
  }
}

class _Footer extends StatelessWidget {
  const _Footer({
    required this.metadata,
  });

  final Metadata metadata;

  @override
  Widget build(BuildContext context) {
    final updates = metadata.refreshUpdates.join(' Â· ');
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppPalette.panel.withValues(alpha: 0.65),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppPalette.border),
      ),
      child: Wrap(
        spacing: 14,
        runSpacing: 10,
        crossAxisAlignment: WrapCrossAlignment.center,
        children: [
          Text(
            'Built with Flutter Web + Python sync automation.',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppPalette.textMuted,
                ),
          ),
          if (metadata.generatedAt.isNotEmpty)
            Text(
              'Generated ${metadata.generatedAt}',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppPalette.textMuted,
                    fontFamily: 'IBMPlexMono',
                  ),
            ),
          if (updates.isNotEmpty)
            Text(
              updates,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppPalette.primarySoft,
                    fontFamily: 'IBMPlexMono',
                  ),
            ),
        ],
      ),
    );
  }
}

class _NavButton extends StatelessWidget {
  const _NavButton({
    required this.label,
    required this.onTap,
  });

  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onTap,
      style: OutlinedButton.styleFrom(
        foregroundColor: AppPalette.text,
        side: BorderSide(color: AppPalette.border.withValues(alpha: 0.9)),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(999),
        ),
      ),
      child: Text(
        label,
        style: const TextStyle(
          fontFamily: 'IBMPlexMono',
          fontWeight: FontWeight.w600,
          fontSize: 12,
        ),
      ),
    );
  }
}

class _SignalPill extends StatelessWidget {
  const _SignalPill({
    required this.label,
    required this.accent,
  });

  final String label;
  final Color accent;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: accent.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: accent.withValues(alpha: 0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: accent,
          fontFamily: 'IBMPlexMono',
          fontSize: 12,
          fontWeight: FontWeight.w600,
          letterSpacing: 1.1,
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  const _ActionButton({
    required this.label,
    required this.icon,
    required this.onTap,
    this.filled = true,
  });

  final String label;
  final IconData icon;
  final VoidCallback onTap;
  final bool filled;

  @override
  Widget build(BuildContext context) {
    final style = filled
        ? FilledButton.styleFrom(
            backgroundColor: AppPalette.primary,
            foregroundColor: AppPalette.background,
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
            ),
          )
        : OutlinedButton.styleFrom(
            foregroundColor: AppPalette.text,
            side: BorderSide(color: AppPalette.border.withValues(alpha: 0.9)),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
            ),
          );

    return filled
        ? FilledButton.icon(
            onPressed: onTap,
            style: style,
            icon: Icon(icon, size: 18),
            label: Text(label),
          )
        : OutlinedButton.icon(
            onPressed: onTap,
            style: style,
            icon: Icon(icon, size: 18),
            label: Text(label),
          );
  }
}

class _MetricTile extends StatelessWidget {
  const _MetricTile({
    required this.label,
    required this.value,
    required this.accent,
  });

  final String label;
  final String value;
  final Color accent;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 140,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppPalette.background.withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppPalette.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label.toUpperCase(),
            style: TextStyle(
              color: accent,
              fontFamily: 'IBMPlexMono',
              fontSize: 11,
              fontWeight: FontWeight.w600,
              letterSpacing: 1.2,
            ),
          ),
          const SizedBox(height: 10),
          Text(
            value,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w700,
                ),
          ),
        ],
      ),
    );
  }
}

class _AvatarBadge extends StatelessWidget {
  const _AvatarBadge({
    required this.avatarUrl,
  });

  final String avatarUrl;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 72,
      height: 72,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
            color: AppPalette.primary.withValues(alpha: 0.35), width: 1.2),
        color: AppPalette.panelSoft,
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(22),
        child: avatarUrl.isEmpty
            ? const Icon(Icons.person_outline_rounded,
                size: 32, color: AppPalette.primarySoft)
            : Image.network(
                avatarUrl,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return const Icon(
                    Icons.person_outline_rounded,
                    size: 32,
                    color: AppPalette.primarySoft,
                  );
                },
              ),
      ),
    );
  }
}

class _CodeFlowBlock extends StatelessWidget {
  const _CodeFlowBlock();

  @override
  Widget build(BuildContext context) {
    final lines = const [
      '> uv run python -m portfolio_app.scripts.sync_data --scope weekly',
      '> uv run python -m portfolio_app.scripts.build_frontend_content',
      '> flutter build web --release --base-href /portfolioMauricioobgo/',
      '> publish build/web -> gh-pages',
    ];

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppPalette.background,
        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: AppPalette.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              _Dot(color: Color(0xFFFF6B6B)),
              SizedBox(width: 8),
              _Dot(color: Color(0xFFFFD166)),
              SizedBox(width: 8),
              _Dot(color: AppPalette.primary),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'deployment.flow',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontFamily: 'IBMPlexMono',
                  color: AppPalette.primarySoft,
                  fontWeight: FontWeight.w600,
                ),
          ),
          const SizedBox(height: 14),
          for (final line in lines) ...[
            Text(
              line,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontFamily: 'IBMPlexMono',
                    color: AppPalette.textMuted,
                    height: 1.7,
                  ),
            ),
            const SizedBox(height: 6),
          ],
        ],
      ),
    );
  }
}

class _Dot extends StatelessWidget {
  const _Dot({required this.color});

  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 10,
      height: 10,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: color,
      ),
    );
  }
}

class _InfoCard extends StatelessWidget {
  const _InfoCard({
    required this.title,
    required this.icon,
    required this.child,
  });

  final String title;
  final IconData icon;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: AppPalette.primarySoft),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            child,
          ],
        ),
      ),
    );
  }
}

class _DataPoint extends StatelessWidget {
  const _DataPoint({
    required this.label,
    required this.value,
  });

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 180,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppPalette.background.withValues(alpha: 0.45),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: AppPalette.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label.toUpperCase(),
            style: const TextStyle(
              fontFamily: 'IBMPlexMono',
              fontSize: 11,
              fontWeight: FontWeight.w600,
              letterSpacing: 1.1,
              color: AppPalette.primarySoft,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            value.isEmpty ? 'not listed' : value,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
          ),
        ],
      ),
    );
  }
}

class _ExperienceCard extends StatelessWidget {
  const _ExperienceCard({
    required this.item,
  });

  final Experience item;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Wrap(
              spacing: 12,
              runSpacing: 12,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: AppPalette.primary.withValues(alpha: 0.08),
                    borderRadius: BorderRadius.circular(999),
                    border: Border.all(
                        color: AppPalette.primary.withValues(alpha: 0.25)),
                  ),
                  child: Text(
                    item.date,
                    style: const TextStyle(
                      color: AppPalette.primarySoft,
                      fontFamily: 'IBMPlexMono',
                      fontWeight: FontWeight.w600,
                      fontSize: 12,
                    ),
                  ),
                ),
                if (item.location.isNotEmpty)
                  Text(
                    item.location,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppPalette.textMuted,
                        ),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              item.role,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 6),
            InkWell(
              onTap: item.companyUrl.isEmpty
                  ? null
                  : () => _launchExternal(item.companyUrl),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    item.company,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: AppPalette.cyan,
                          fontWeight: FontWeight.w600,
                        ),
                  ),
                  if (item.companyUrl.isNotEmpty) ...[
                    const SizedBox(width: 8),
                    const Icon(Icons.open_in_new_rounded,
                        size: 18, color: AppPalette.cyan),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 16),
            Text(
              item.description,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppPalette.textMuted,
                    height: 1.7,
                  ),
            ),
            if (item.highlights.isNotEmpty) ...[
              const SizedBox(height: 18),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: item.highlights
                    .map((highlight) => Chip(label: Text(highlight)))
                    .toList(),
              ),
            ],
            if (item.referenceUrl.isNotEmpty) ...[
              const SizedBox(height: 18),
              TextButton.icon(
                onPressed: () => _launchExternal(item.referenceUrl),
                icon: const Icon(Icons.link_rounded, size: 18),
                label: Text(
                  item.referenceLabel.isEmpty
                      ? 'View reference'
                      : item.referenceLabel,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _ProjectCard extends StatelessWidget {
  const _ProjectCard({
    required this.project,
  });

  final Project project;

  @override
  Widget build(BuildContext context) {
    final tags = project.tags.isEmpty
        ? const ['cloud systems', 'analytics', 'delivery']
        : project.tags;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'featured_work',
              style: TextStyle(
                fontFamily: 'IBMPlexMono',
                color: AppPalette.primarySoft,
                fontSize: 12,
                fontWeight: FontWeight.w600,
                letterSpacing: 1.1,
              ),
            ),
            const SizedBox(height: 14),
            Text(
              project.name,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
            ),
            const SizedBox(height: 12),
            Text(
              project.summary,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppPalette.textMuted,
                    height: 1.7,
                  ),
            ),
            const SizedBox(height: 18),
            Wrap(
              spacing: 10,
              runSpacing: 10,
              children: tags.map((tag) => Chip(label: Text(tag))).toList(),
            ),
            if (project.impact.isNotEmpty) ...[
              const SizedBox(height: 18),
              Text(
                project.impact,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppPalette.warning,
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ],
            if (project.link.isNotEmpty) ...[
              const SizedBox(height: 18),
              TextButton.icon(
                onPressed: () => _launchExternal(project.link),
                icon: const Icon(Icons.north_east_rounded, size: 18),
                label: const Text('Open project'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _RepoCard extends StatelessWidget {
  const _RepoCard({
    required this.repo,
  });

  final GithubRepository repo;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: () => _launchExternal(repo.htmlUrl),
        borderRadius: BorderRadius.circular(28),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.terminal_rounded,
                      color: AppPalette.primarySoft),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      repo.name,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.w700,
                          ),
                    ),
                  ),
                  const Icon(Icons.open_in_new_rounded,
                      size: 18, color: AppPalette.textMuted),
                ],
              ),
              const SizedBox(height: 14),
              Text(
                repo.description.isEmpty
                    ? 'Repository activity synced from GitHub.'
                    : repo.description,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: AppPalette.textMuted,
                      height: 1.7,
                    ),
              ),
              const SizedBox(height: 18),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  _InlineStat(
                      label: 'Updated', value: _readableDate(repo.updatedAt)),
                  _InlineStat(label: 'Stars', value: '${repo.stargazersCount}'),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _CertificationCard extends StatelessWidget {
  const _CertificationCard({
    required this.certification,
  });

  final Certification certification;

  @override
  Widget build(BuildContext context) {
    final isAws = certification.title.contains('AWS Certified');
    final accent = isAws ? AppPalette.warning : AppPalette.primarySoft;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: accent.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: accent.withValues(alpha: 0.3)),
              ),
              child: Text(
                isAws ? 'AWS TRACK' : 'CERTIFIED',
                style: TextStyle(
                  color: accent,
                  fontFamily: 'IBMPlexMono',
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1.1,
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text(
              certification.title,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w700,
                    height: 1.2,
                  ),
            ),
            const SizedBox(height: 10),
            Text(
              certification.issuer,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppPalette.cyan,
                    fontWeight: FontWeight.w600,
                  ),
            ),
            const SizedBox(height: 12),
            Text(
              certification.issued,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppPalette.textMuted,
                    fontFamily: 'IBMPlexMono',
                  ),
            ),
            if (certification.credentialId.isNotEmpty) ...[
              const SizedBox(height: 10),
              Text(
                'Credential ID: ${certification.credentialId}',
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppPalette.textMuted,
                      fontFamily: 'IBMPlexMono',
                    ),
              ),
            ],
            const SizedBox(height: 18),
            TextButton.icon(
              onPressed: () => _launchExternal(certification.credentialUrl),
              icon: const Icon(Icons.verified_outlined, size: 18),
              label: Text(
                certification.credentialLabel.isEmpty
                    ? 'View credential'
                    : certification.credentialLabel,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ContactCard extends StatelessWidget {
  const _ContactCard({
    required this.title,
    required this.value,
    required this.caption,
    required this.onTap,
  });

  final String title;
  final String value;
  final String caption;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(28),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title.toUpperCase(),
                style: const TextStyle(
                  color: AppPalette.primarySoft,
                  fontFamily: 'IBMPlexMono',
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  letterSpacing: 1.1,
                ),
              ),
              const SizedBox(height: 14),
              Text(
                value,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w700,
                    ),
              ),
              const SizedBox(height: 12),
              Text(
                caption,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: AppPalette.textMuted,
                      height: 1.7,
                    ),
              ),
              const SizedBox(height: 18),
              const Row(
                children: [
                  Icon(Icons.north_east_rounded, color: AppPalette.cyan),
                  SizedBox(width: 8),
                  Text(
                    'Open',
                    style: TextStyle(
                      color: AppPalette.cyan,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InlineStat extends StatelessWidget {
  const _InlineStat({
    required this.label,
    required this.value,
  });

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: AppPalette.background.withValues(alpha: 0.45),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppPalette.border),
      ),
      child: RichText(
        text: TextSpan(
          children: [
            TextSpan(
              text: '$label: ',
              style: const TextStyle(
                fontFamily: 'IBMPlexMono',
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: AppPalette.primarySoft,
              ),
            ),
            TextSpan(
              text: value,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppPalette.text,
                    fontWeight: FontWeight.w600,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

class _AnchoredSection extends StatelessWidget {
  const _AnchoredSection({
    required this.sectionKey,
    required this.child,
  });

  final GlobalKey sectionKey;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      key: sectionKey,
      child: child,
    );
  }
}

Future<void> _launchExternal(String url) async {
  if (url.isEmpty) {
    return;
  }
  final uri = Uri.parse(url);
  await launchUrl(uri, mode: LaunchMode.platformDefault);
}

String _readableDate(String value) {
  if (value.length >= 10) {
    return value.substring(0, 10);
  }
  return value;
}
