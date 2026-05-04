class PortfolioContent {
  const PortfolioContent({
    required this.metadata,
    required this.profile,
    required this.experience,
    required this.projects,
    required this.certifications,
    required this.github,
  });

  factory PortfolioContent.fromJson(Map<String, dynamic> json) {
    return PortfolioContent(
      metadata: Metadata.fromJson(_asMap(json['metadata'])),
      profile: Profile.fromJson(_asMap(json['profile'])),
      experience: _asList(json['experience']).map(Experience.fromJson).toList(),
      projects: _asList(json['projects']).map(Project.fromJson).toList(),
      certifications:
          _asList(json['certifications']).map(Certification.fromJson).toList(),
      github: GithubData.fromJson(_asMap(json['github'])),
    );
  }

  final Metadata metadata;
  final Profile profile;
  final List<Experience> experience;
  final List<Project> projects;
  final List<Certification> certifications;
  final GithubData github;
}

class Metadata {
  const Metadata({
    required this.generatedAt,
    required this.frontend,
    required this.refreshScope,
    required this.refreshUpdates,
  });

  factory Metadata.fromJson(Map<String, dynamic> json) {
    final refreshLog = _asMap(json['refresh_log']);
    return Metadata(
      generatedAt: json['generated_at']?.toString() ?? '',
      frontend: json['frontend']?.toString() ?? '',
      refreshScope: refreshLog['scope']?.toString() ?? '',
      refreshUpdates: _stringList(refreshLog['updates']),
    );
  }

  final String generatedAt;
  final String frontend;
  final String refreshScope;
  final List<String> refreshUpdates;
}

class Profile {
  const Profile({
    required this.name,
    required this.title,
    required this.subtitle,
    required this.about,
    required this.resumeLink,
    required this.email,
    required this.socialLinks,
    required this.skills,
    required this.githubUrl,
    required this.linkedinCertificationsUrl,
    required this.avatarUrl,
    required this.location,
    required this.company,
    required this.bio,
    required this.githubFollowers,
    required this.githubPublicRepos,
    required this.githubUpdatedAt,
  });

  factory Profile.fromJson(Map<String, dynamic> json) {
    final socialLinks = _asMap(json['social_links']).map(
      (key, value) => MapEntry(key, value?.toString() ?? ''),
    );
    return Profile(
      name: json['name']?.toString() ?? '',
      title: json['title']?.toString() ?? '',
      subtitle: json['subtitle']?.toString() ?? '',
      about: json['about']?.toString() ?? '',
      resumeLink: json['resume_link']?.toString() ?? '',
      email: json['email']?.toString() ?? '',
      socialLinks: socialLinks,
      skills: _stringList(json['skills']),
      githubUrl: json['github_url']?.toString() ?? '',
      linkedinCertificationsUrl:
          json['linkedin_certifications_url']?.toString() ?? '',
      avatarUrl: json['avatar_url']?.toString() ?? '',
      location: json['location']?.toString() ?? '',
      company: json['company']?.toString() ?? '',
      bio: json['bio']?.toString() ?? '',
      githubFollowers: _asInt(json['github_followers']),
      githubPublicRepos: _asInt(json['github_public_repos']),
      githubUpdatedAt: json['github_updated_at']?.toString() ?? '',
    );
  }

  final String name;
  final String title;
  final String subtitle;
  final String about;
  final String resumeLink;
  final String email;
  final Map<String, String> socialLinks;
  final List<String> skills;
  final String githubUrl;
  final String linkedinCertificationsUrl;
  final String avatarUrl;
  final String location;
  final String company;
  final String bio;
  final int githubFollowers;
  final int githubPublicRepos;
  final String githubUpdatedAt;
}

class Experience {
  const Experience({
    required this.role,
    required this.company,
    required this.date,
    required this.location,
    required this.description,
    required this.highlights,
    required this.companyUrl,
    required this.referenceUrl,
    required this.referenceLabel,
  });

  factory Experience.fromJson(Map<String, dynamic> json) {
    return Experience(
      role: json['role']?.toString() ?? '',
      company: json['company']?.toString() ?? '',
      date: json['date']?.toString() ?? '',
      location: json['location']?.toString() ?? '',
      description: json['description']?.toString() ?? '',
      highlights: _stringList(json['highlights']),
      companyUrl: json['company_url']?.toString() ?? '',
      referenceUrl: json['reference_url']?.toString() ?? '',
      referenceLabel: json['reference_label']?.toString() ?? '',
    );
  }

  final String role;
  final String company;
  final String date;
  final String location;
  final String description;
  final List<String> highlights;
  final String companyUrl;
  final String referenceUrl;
  final String referenceLabel;
}

class Project {
  const Project({
    required this.name,
    required this.summary,
    required this.link,
    required this.tags,
    required this.impact,
  });

  factory Project.fromJson(Map<String, dynamic> json) {
    return Project(
      name: json['name']?.toString() ?? '',
      summary: json['summary']?.toString() ?? '',
      link: json['link']?.toString() ?? '',
      tags: _stringList(json['tags']),
      impact: json['impact']?.toString() ?? '',
    );
  }

  final String name;
  final String summary;
  final String link;
  final List<String> tags;
  final String impact;
}

class Certification {
  const Certification({
    required this.title,
    required this.issuer,
    required this.issued,
    required this.credentialId,
    required this.credentialUrl,
    required this.credentialLabel,
  });

  factory Certification.fromJson(Map<String, dynamic> json) {
    return Certification(
      title: json['title']?.toString() ?? '',
      issuer: json['issuer']?.toString() ?? '',
      issued: json['issued']?.toString() ?? '',
      credentialId: json['credential_id']?.toString() ?? '',
      credentialUrl: json['credential_url']?.toString() ?? '',
      credentialLabel: json['credential_label']?.toString() ?? '',
    );
  }

  final String title;
  final String issuer;
  final String issued;
  final String credentialId;
  final String credentialUrl;
  final String credentialLabel;
}

class GithubData {
  const GithubData({
    required this.profile,
    required this.repositories,
  });

  factory GithubData.fromJson(Map<String, dynamic> json) {
    return GithubData(
      profile: GithubProfile.fromJson(_asMap(json['profile'])),
      repositories:
          _asList(json['repositories']).map(GithubRepository.fromJson).toList(),
    );
  }

  final GithubProfile profile;
  final List<GithubRepository> repositories;
}

class GithubProfile {
  const GithubProfile({
    required this.login,
    required this.name,
    required this.company,
    required this.location,
    required this.bio,
    required this.avatarUrl,
    required this.htmlUrl,
    required this.followers,
    required this.publicRepos,
    required this.updatedAt,
  });

  factory GithubProfile.fromJson(Map<String, dynamic> json) {
    return GithubProfile(
      login: json['login']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      company: json['company']?.toString() ?? '',
      location: json['location']?.toString() ?? '',
      bio: json['bio']?.toString() ?? '',
      avatarUrl: json['avatar_url']?.toString() ?? '',
      htmlUrl: json['html_url']?.toString() ?? '',
      followers: _asInt(json['followers']),
      publicRepos: _asInt(json['public_repos']),
      updatedAt: json['updated_at']?.toString() ?? '',
    );
  }

  final String login;
  final String name;
  final String company;
  final String location;
  final String bio;
  final String avatarUrl;
  final String htmlUrl;
  final int followers;
  final int publicRepos;
  final String updatedAt;
}

class GithubRepository {
  const GithubRepository({
    required this.name,
    required this.htmlUrl,
    required this.description,
    required this.updatedAt,
    required this.stargazersCount,
  });

  factory GithubRepository.fromJson(Map<String, dynamic> json) {
    return GithubRepository(
      name: json['name']?.toString() ?? '',
      htmlUrl: json['html_url']?.toString() ?? '',
      description: json['description']?.toString() ?? '',
      updatedAt: json['updated_at']?.toString() ?? '',
      stargazersCount: _asInt(json['stargazers_count']),
    );
  }

  final String name;
  final String htmlUrl;
  final String description;
  final String updatedAt;
  final int stargazersCount;
}

Map<String, dynamic> _asMap(Object? value) {
  if (value is Map<String, dynamic>) {
    return value;
  }
  if (value is Map) {
    return value.map(
      (key, mapValue) => MapEntry(key.toString(), mapValue),
    );
  }
  return const {};
}

List<Map<String, dynamic>> _asList(Object? value) {
  if (value is List) {
    return value.map((item) => _asMap(item)).toList();
  }
  return const [];
}

List<String> _stringList(Object? value) {
  if (value is List) {
    return value
        .map((item) => item.toString())
        .where((item) => item.isNotEmpty)
        .toList();
  }
  return const [];
}

int _asInt(Object? value) {
  if (value is int) {
    return value;
  }
  return int.tryParse(value?.toString() ?? '') ?? 0;
}
