/* Change this file to get your personal Portfolio */

// To change portfolio colors globally go to the  _globalColor.scss file

import emoji from "react-easy-emoji";
import splashAnimation from "./assets/lottie/splashAnimation"; // Rename to your file name for custom animation

// Splash Screen

const splashScreen = {
  enabled: true, // set false to disable splash screen
  animation: splashAnimation,
  duration: 2000 // Set animation duration as per your animation
};

// Summary And Greeting Section

const illustration = {
  animated: true // Set to false to use static SVG
};

const greeting = {
  username: "Mauricio Obando",
  title: "Hi all, I am Mauricio",
  subTitle: emoji(
    "😄 My Passion for Data Engineering, Data Science, and the Cloud ☁️ I'm absolutely thrilled about working with data, whether it's in the realm of Data Engineering, Data Science, or leveraging the power of the cloud. The convergence of these fields adds immense excitement to my work! In this data-driven world, I'm enthusiastic about applying my skills to drive innovation and make meaningful contributions! 🌍📊"
  ),
  resumeLink:
    "https://drive.google.com/file/d/1P3lCrfvF0V34HSASe8YdKTUgh-VDPZzt/view?usp=sharing", // Set to empty to hide the button
  displayGreeting: true // Set false to hide this section, defaults to true
};

// Social Media Links

const socialMediaLinks = {
  github: "https://github.com/mauricioobgo",
  linkedin: "https://www.linkedin.com/in/mauricio-obando-06456160/",
  gmail: "mauricioobgo@gmail.com",
  // Instagram, Twitter and Kaggle are also supported in the links!
  // To customize icons and social links, tweak src/components/SocialMedia
  display: true // Set true to display this section, defaults to false
};

// Skills Section

const skillsSection = {
  title: "What I Love to do",
  subTitle: "CRAZY DataScientist and Data Engineer who wants to explore the world through data 🌍",
  skills: [
    emoji(
      "⚡ 💡 Data Engineering and DataScience allows me to shape raw data into valuable insights."
    ),
    emoji("⚡ 🌐 Cloud providers like AWS, Azure, and GCP provide the scalable infrastructure I need."),
    emoji(
      "⚡ With ☁️ services, I can process, store, and analyze data in various creative ways."
    ),
    emoji(
      "⚡ Also  If I want to Ingest Data I could use different frameworks like hadoop or spark to process and transform data"
    ),
    emoji(
      "⚡ And if there is a useful tool like dbt that helps me transform data and create jobs to trigger those transformations I normally use it."
    ),
  ],

  /* Make Sure to include correct Font Awesome Classname to view your icon
https://fontawesome.com/icons?d=gallery */

  softwareSkills: [
    {
      skillName: "JavaScript",
      fontAwesomeClassname: "fab fa-js"
    },
    {
      skillName: "nodejs",
      fontAwesomeClassname: "fab fa-node"
    },
    {
      skillName: "npm",
      fontAwesomeClassname: "fab fa-npm"
    },
    {
      skillName: "Warehousing",
      fontAwesomeClassname: "fas fa-database"
    },
    {
      skillName: "aws",
      fontAwesomeClassname: "fab fa-aws"
    },
    {
      skillName: "GCP",
      fontAwesomeClassname: "fab fa-google"
    },
    {
      skillName: "firebase",
      fontAwesomeClassname: "fas fa-fire"
    },
    {
      skillName: "python",
      fontAwesomeClassname: "fab fa-python"
    },
    {
      skillName: "docker",
      fontAwesomeClassname: "fab fa-docker"
    },
    {
      skillName: "Spark",
      fontAwesomeClassname: "far fa-star"
    }
    
  ],
  display: true // Set false to hide this section, defaults to true
};

// Education Section

const educationInfo = {
  display: true, // Set false to hide this section, defaults to true
  schools: [
    {
      schoolName: "Universitat Ramon Llull",
      logo: require("./assets/images/ramonllull_logo.png"),
      subHeader: "Master in Wealth and Financial Management",
      duration: "September 2018 - September 2020",
      desc: "Financial Planning and Econometric Analysis",
      descBullets: [
        "Quantitative Finance Oriented Degree"
      ]
    },
    {
      schoolName: "Universidad de La Sabana",
      logo: require("./assets/images/universidad_de_la_sabana.png"),
      subHeader: "Master in Investment Management",
      duration: "September 2018 - September 2020",
      desc: "Program focused on Quantitavie Market Analysis",
      descBullets: ["Quantitative Analysis and Data Analysis"]
    }
  ]
};

// Your top 3 proficient stacks/tech experience

const techStack = {
  viewSkillBars: true, //Set it to true to show Proficiency Section
  experience: [
    {
      Stack: "Frontend/Design", //Insert stack or technology you have experience in
      progressPercentage: "30%" //Insert relative proficiency in percentage
    },
    {
      Stack: "Backend",
      progressPercentage: "80%"
    },
    {
      Stack: "Python Programming",
      progressPercentage: "80%"
    }
    ,
    {
      Stack: "Spark",
      progressPercentage: "80%"
    }
    ,
    {
      Stack: "AWS",
      progressPercentage: "80%"
    }
    ,
    {
      Stack: "GCP",
      progressPercentage: "60%"
    }
  ],
  displayCodersrank: false // Set true to display codersrank badges section need to changes your username in src/containers/skillProgress/skillProgress.js:17:62, defaults to false
};

// Work experience section

const workExperiences = {
  display: true, //Set it to true to show workExperiences Section
  experience: [
    {
      role: "Lead Data Engineer",
      company: "Publicis Groupe",
      companylogo: require("./assets/images/publicis_groupe.png"),
      date: "Feb 2023 – Present",
      desc: "Developed critical, efficient data pipelines for Stellantis as well as lead implementations of Referenced Architectures for data pipelines implementation using GCP and AWS",
      descBullets: [
        "Create Architecture solutions for Dashboards, using Tableau and looker and all the Data ingestion and transformation pipelines in order to create insights for the DataScience team.",
        "Propose solutions for monitoring different pipelines in order to adjust billing and all the framework usage in each individual case so that it could standardize performance and homologate versions in terms of software."
      ]
    },
    {
      role: "Senior Data Scientist, Data Architect",
      company: "Globant",
      companylogo: require("./assets/images/globant.png"),
      date: "July 2021 – Feb 2023",
      desc: "Data Engineer also assuming the role of Data Scientist to solve MLOPs problems as well as Infrastructure design for Data pipelines solutions on AWS services"
    },
    {
      role: "Sr. Data Analyst",
      company: "PDG | Publicis Groupe",
      companylogo: require("./assets/images/pgd.png"),
      date: "Sep 2020 – July 2021",
      desc: "Develope Pipelines for Marketing Mix models and creating their respective CICD training Pipelines"
    }
  ]
};

/* Your Open Source Section to View Your Github Pinned Projects
To know how to get github key look at readme.md */

const openSource = {
  showGithubProfile: "true", // Set true or false to show Contact profile using Github, defaults to true
  display: true // Set false to hide this section, defaults to true
};

// Some big projects you have worked on

const bigProjects = {
  title: "Big Projects",
  subtitle: "SOME OF THE BIG PROJECTS I'VE WORKED ON",
  projects: [
    {
      image: require("./assets/images/disney.png"),
      projectName: "COP (COMMERCIAL OPTIMIZATION PLATFORM)",
      projectDesc: " Centralizing, building and gather Data In Snowflake from Different Sources within The World Disney Company",
/*       footerLink: [
        {
          name: "Visit Website",
          url: "http://saayahealth.com/"
        }
        //  you can add extra buttons here.
      ] */
    },
    {
      image: require("./assets/images/disney.png"),
      projectName: "Food and Beverage Recomendation Model",
      projectDesc: "Create MlOPs pipeline for dining recomendation model within the each restaurant within Orlando Parks",
      /* footerLink: [
        {
          name: "Visit Website",
          url: "http://nextu.se/"
        }
      ] */
    }
  ],
  display: true // Set false to hide this section, defaults to true
};

// Achievement Section
// Include certificates, talks etc

const achievementSection = {
  title: emoji("Achievements And Certifications 🏆 "),
  subtitle:
    "Achievements, Certifications, Award Letters and Some Cool Stuff that I have done !",

  achievementsCards: [
    {
      title: "AWS Architect Associate",
      subtitle:
        "Earners of this certification have a comprehensive understanding of AWS services and technologies. They demonstrated the ability to build secure and robust solutions using architectural design principles based on customer requirements. Badge owners are able to strategically design well-architected distributed systems that are scalable, resilient, efficient, and fault-tolerant.",
      image: require("./assets/images/aws_architect_associate.png"),
      imageAlt: "Google Code-In Logo",
      footerLink: [
        {
          name: "Certification",
          url: "https://www.credly.com/badges/682ec0ed-813d-44d1-b4af-b1cc7f277135/linked_in_profile"
        }
      ]
    },
    {
      title: "DS4A / Colombia 6.0",
      subtitle:
        "The certificate earner has graduated from the Data Science For All (DS4A) program as part of the Colombia 2022 cohort. They are ready for a career in data science and have learned how to work with Jupyter notebooks, use Python libraries to generate data visualizations, perform exploratory data analysis, and analyze data using Pandas. They also learned the use of different Data Science and AI techniques, such as Decision Trees and the use of kNNs, CNNs, NLP, along with how to practically utilize them.",
      image: require("./assets/images/ds4a.png"),
      imageAlt: "Google Assistant Action Logo",
      footerLink: [
        {
          name: "Certification",
          url: "https://www.credential.net/29692783-9c88-486d-95a7-f460bf1730bb"
        },
        {
          name: "Award Letter",
          url: "https://www.credential.net/91812129-81fc-4d5e-97dd-c1ec3ed03bf1"
        },
        {
          name: "Final Project",
          url: "https://github.com/mauricioobgo/ds4aDashApp"
        }
      ]
    },

    {
      title: "Deep Learning",
      subtitle: "Completed Certifcation from Deep Learning AI company",
      image: require("./assets/images/deep_learning_ai.png"),
      imageAlt: "PWA Logo",
      footerLink: [
        {name: "Certification", url: "https://coursera.org/share/95cf7a3d427261ccf07952cf0fbfa800"}
      ]
    }
  ],
  display: true // Set false to hide this section, defaults to true
};

// Blogs Section

const blogSection = {
  title: "Blogs",
  subtitle:
    "With Love for Developing cool stuff, I love to write and teach others what I have learnt.",
  displayMediumBlogs: "true", // Set true to display fetched medium blogs instead of hardcoded ones
  blogs: [
/*     {
      url: "https://blog.usejournal.com/create-a-google-assistant-action-and-win-a-google-t-shirt-and-cloud-credits-4a8d86d76eae",
      title: "Win a Google Assistant Tshirt and $200 in Google Cloud Credits",
      description:
        "Do you want to win $200 and Google Assistant Tshirt by creating a Google Assistant Action in less then 30 min?"
    },
    {
      url: "https://medium.com/@saadpasta/why-react-is-the-best-5a97563f423e",
      title: "Why REACT is The Best?",
      description:
        "React is a JavaScript library for building User Interface. It is maintained by Facebook and a community of individual developers and companies."
    } */
  ],
  display: false // Set false to hide this section, defaults to true
};

// Talks Sections

const talkSection = {
  title: "TALKS",
  subtitle: emoji(
    "I LOVE TO SHARE MY LIMITED KNOWLEDGE AND GET A SPEAKER BADGE 😅"
  ),

/*   talks: [
    {
      title: "Build Actions For Google Assistant",
      subtitle: "Codelab at GDG DevFest Karachi 2019",
      slides_url: "https://bit.ly/saadpasta-slides",
      event_url: "https://www.facebook.com/events/2339906106275053/"
    }
  ], */
  display: false // Set false to hide this section, defaults to true
};

// Podcast Section

const podcastSection = {
  title: emoji("Podcast 🎙️"),
  subtitle: "I LOVE TO TALK ABOUT MYSELF AND TECHNOLOGY",

  // Please Provide with Your Podcast embeded Link
/*   podcast: [
    "https://anchor.fm/codevcast/embed/episodes/DevStory---Saad-Pasta-from-Karachi--Pakistan-e9givv/a-a15itvo"
  ], */
  display: false // Set false to hide this section, defaults to true
};

const contactInfo = {
  title: emoji("Contact Me ☎️"),
  subtitle:
    "Discuss a project or just want to say hi? My Inbox is open for all.",
  number: "+57-3156378510",
  email_address: "mauricioobgo@gmail.com"
};

// Twitter Section

const twitterDetails = {
  userName: "twitter", //Replace "twitter" with your twitter username without @
  display: false // Set true to display this section, defaults to false
};

const isHireable = false; // Set false if you are not looking for a job. Also isHireable will be display as Open for opportunities: Yes/No in the GitHub footer

export {
  illustration,
  greeting,
  socialMediaLinks,
  splashScreen,
  skillsSection,
  educationInfo,
  techStack,
  workExperiences,
  openSource,
  bigProjects,
  achievementSection,
  blogSection,
  talkSection,
  podcastSection,
  contactInfo,
  twitterDetails,
  isHireable
};
