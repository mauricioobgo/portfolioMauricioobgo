import 'package:flutter_test/flutter_test.dart';

import 'package:portfolio_flutter_site/app.dart';
import 'package:portfolio_flutter_site/models/portfolio_content.dart';
import 'package:portfolio_flutter_site/services/portfolio_repository.dart';

void main() {
  testWidgets('renders core portfolio sections from repository data',
      (tester) async {
    await tester.pumpWidget(
      PortfolioApp(
        repository: _FakePortfolioRepository(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Mauricio Obando'), findsWidgets);
    expect(find.text('Senior Data Engineer'), findsOneWidget);
    expect(find.text('AWS Certified Solutions Architect - Professional'),
        findsOneWidget);
    expect(find.text('portfolioMauricioobgo'), findsOneWidget);
  });
}

class _FakePortfolioRepository implements PortfolioRepository {
  @override
  Future<PortfolioContent> load() async {
    return PortfolioContent(
      metadata: const Metadata(
        generatedAt: '2026-05-03T00:00:00+00:00',
        frontend: 'flutter',
        refreshScope: 'all',
        refreshUpdates: ['github_repositories_weekly'],
      ),
      profile: const Profile(
        name: 'Mauricio Obando',
        title: 'AI-Ready Data Engineer',
        subtitle:
            'Building cloud pipelines, analytics systems, and practical AI workflows.',
        about:
            'Senior data engineer with 7+ years across cloud architecture and AI delivery.',
        resumeLink: 'https://example.com/resume',
        email: 'mauricioobgo@gmail.com',
        socialLinks: {
          'github': 'https://github.com/mauricioobgo',
          'linkedin': 'https://www.linkedin.com/in/mauricioobgo/',
        },
        skills: ['Python', 'Flutter', 'AWS'],
        githubUrl: 'https://github.com/mauricioobgo',
        linkedinCertificationsUrl:
            'https://www.linkedin.com/in/mauricioobgo/details/certifications/',
        avatarUrl: '',
        location: 'Bogota, Colombia',
        company: 'Globant',
        bio: 'Generated bio',
        githubFollowers: 7,
        githubPublicRepos: 35,
        githubUpdatedAt: '2026-05-03T00:00:00Z',
      ),
      experience: const [
        Experience(
          role: 'Senior Data Engineer',
          company: 'Globant',
          date: '2025 - Present',
          location: 'Bogota, Colombia',
          description: 'Leading cloud and AI delivery work.',
          highlights: ['Production AI pilots'],
          companyUrl: 'https://www.globant.com/',
          referenceUrl: 'https://www.linkedin.com/in/mauricioobgo/',
          referenceLabel: 'LinkedIn profile',
        ),
      ],
      projects: const [
        Project(
          name: 'Commercial Optimization Platform',
          summary:
              'Cloud-native optimization platform for commercial performance.',
          link: '',
          tags: ['python', 'aws'],
          impact: '',
        ),
      ],
      certifications: const [
        Certification(
          title: 'AWS Certified Solutions Architect - Professional',
          issuer: 'Amazon Web Services',
          issued: 'Listed on LinkedIn',
          credentialId: '',
          credentialUrl:
              'https://www.linkedin.com/in/mauricioobgo/details/certifications/',
          credentialLabel: 'View on LinkedIn',
        ),
      ],
      github: const GithubData(
        profile: GithubProfile(
          login: 'mauricioobgo',
          name: 'Mauricio Obando',
          company: 'Globant',
          location: 'Bogota, Colombia',
          bio: 'Generated bio',
          avatarUrl: '',
          htmlUrl: 'https://github.com/mauricioobgo',
          followers: 7,
          publicRepos: 35,
          updatedAt: '2026-05-03T00:00:00Z',
        ),
        repositories: [
          GithubRepository(
            name: 'portfolioMauricioobgo',
            htmlUrl: 'https://github.com/mauricioobgo/portfolioMauricioobgo',
            description: 'Portfolio source',
            updatedAt: '2026-05-03T00:00:00Z',
            stargazersCount: 0,
          ),
        ],
      ),
    );
  }
}
