#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const SKILLS = [
  "docs-init",
  "docs-executor",
  "docs-plan-ap",
  "docs-plan-sddr",
  "docs-reviewer",
];

const LEGACY_CODEX_SKILLS = [
  "xml-docs-init-executor",
  "xml-docs-init-plan-ap",
  "xml-docs-init-plan-sddr",
  "xml-docs-init-reviewer",
];

class InstallError extends Error {}

function usage() {
  console.log(`Install DOCS skills.

Usage:
  npx --yes github:nckprojetos1-sketch/docs-skills
  npx --yes github:nckprojetos1-sketch/docs-skills update

Options:
  --codex-skills <path>   Target Codex skills directory. Defaults to ~/.codex/skills.
  --agents-skills <path>  Target Agents skills directory. Defaults to ~/.agents/skills.
  --keep-legacy           Do not disable xml-docs-init-* legacy skills.
  --clean-docs            Move any installed docs-* or xml-docs-* skill not in this package.
  -h, --help              Show this help message.
`);
}

function parseArgs(argv) {
  const args = {
    codexSkills: path.join(os.homedir(), ".codex", "skills"),
    agentsSkills: path.join(os.homedir(), ".agents", "skills"),
    keepLegacy: false,
    cleanDocs: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (current === "install" || current === "update") {
      continue;
    }
    if (current === "-h" || current === "--help") {
      usage();
      process.exit(0);
    }
    if (current === "--keep-legacy") {
      args.keepLegacy = true;
      continue;
    }
    if (current === "--clean-docs") {
      args.cleanDocs = true;
      continue;
    }
    if (current === "--codex-skills" || current === "--agents-skills") {
      const value = argv[i + 1];
      if (!value || value.startsWith("--")) {
        throw new InstallError(`Missing value for ${current}`);
      }
      if (current === "--codex-skills") {
        args.codexSkills = value;
      } else {
        args.agentsSkills = value;
      }
      i += 1;
      continue;
    }
    throw new InstallError(`Unknown argument: ${current}`);
  }

  args.codexSkills = path.resolve(args.codexSkills.replace(/^~/, os.homedir()));
  args.agentsSkills = path.resolve(args.agentsSkills.replace(/^~/, os.homedir()));
  return args;
}

function timestamp() {
  const pad = (value) => String(value).padStart(2, "0");
  const now = new Date();
  return [
    now.getFullYear(),
    pad(now.getMonth() + 1),
    pad(now.getDate()),
    "-",
    pad(now.getHours()),
    pad(now.getMinutes()),
    pad(now.getSeconds()),
  ].join("");
}

function copyTree(source, destination, backupRoot) {
  if (!fs.existsSync(source) || !fs.statSync(source).isDirectory()) {
    throw new InstallError(`Missing source skill: ${source}`);
  }

  let action = "created";
  if (fs.existsSync(destination)) {
    action = "updated";
    if (backupRoot) {
      fs.mkdirSync(backupRoot, { recursive: true });
      const backupDestination = path.join(backupRoot, path.basename(destination));
      if (fs.existsSync(backupDestination)) {
        throw new InstallError(`Backup path already exists: ${backupDestination}`);
      }
      fs.cpSync(destination, backupDestination, { recursive: true });
    }
    fs.rmSync(destination, { recursive: true, force: true });
  }

  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(source, destination, { recursive: true });
  return action;
}

function validateSkill(skillDir) {
  const errors = [];
  const name = path.basename(skillDir);
  const skillMd = path.join(skillDir, "SKILL.md");
  if (!fs.existsSync(skillMd)) {
    return [`${name}: missing SKILL.md`];
  }

  const text = fs.readFileSync(skillMd, "utf8");
  if (!text.startsWith("---\n")) {
    errors.push(`${name}: missing YAML frontmatter`);
  }
  if (!text.includes(`name: ${name}`)) {
    errors.push(`${name}: frontmatter name mismatch`);
  }
  if (!text.includes("description:")) {
    errors.push(`${name}: missing description`);
  }
  if (text.includes("[TODO")) {
    errors.push(`${name}: contains TODO placeholder`);
  }

  const openaiYaml = path.join(skillDir, "agents", "openai.yaml");
  if (!fs.existsSync(openaiYaml)) {
    errors.push(`${name}: missing agents/openai.yaml`);
  } else {
    const yamlText = fs.readFileSync(openaiYaml, "utf8");
    if (!yamlText.includes("allow_implicit_invocation: false")) {
      errors.push(`${name}: explicit invocation policy missing`);
    }
  }

  return errors;
}

function validateAll(skillDirs) {
  return skillDirs.flatMap(validateSkill);
}

function moveSkill(source, destination) {
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  if (fs.existsSync(destination)) {
    throw new InstallError(`Destination already exists: ${destination}`);
  }
  fs.renameSync(source, destination);
}

function disableLegacy(codexSkills, disabledRoot) {
  const moved = [];
  fs.mkdirSync(disabledRoot, { recursive: true });
  for (const name of LEGACY_CODEX_SKILLS) {
    const source = path.join(codexSkills, name);
    if (!fs.existsSync(source)) {
      continue;
    }
    const destination = path.join(disabledRoot, name);
    moveSkill(source, destination);
    moved.push(destination);
  }
  return moved;
}

function cleanDocsSkills(targetRoot, disabledRoot) {
  if (!fs.existsSync(targetRoot)) {
    return [];
  }

  const moved = [];
  fs.mkdirSync(disabledRoot, { recursive: true });
  const entries = fs.readdirSync(targetRoot, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }
    const isDocsSkill = entry.name.startsWith("docs-") || entry.name.startsWith("xml-docs-");
    const isCurrentSkill = SKILLS.includes(entry.name);
    if (!isDocsSkill || isCurrentSkill) {
      continue;
    }
    const source = path.join(targetRoot, entry.name);
    const destination = path.join(disabledRoot, entry.name);
    moveSkill(source, destination);
    moved.push(destination);
  }
  return moved;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = path.resolve(__dirname, "..");
  const sourceRoot = path.join(root, "skills");
  const stamp = timestamp();
  const backupRoot = path.join(path.dirname(args.codexSkills), "skills-backups", stamp);

  const sourceDirs = SKILLS.map((name) => path.join(sourceRoot, name));
  const sourceErrors = validateAll(sourceDirs);
  if (sourceErrors.length > 0) {
    throw new InstallError(`Source validation failed: ${sourceErrors.join("; ")}`);
  }

  const installed = {};
  const disabled = [];
  const codexInstalledDirs = [];

  if (args.cleanDocs) {
    disabled.push(
      ...cleanDocsSkills(args.codexSkills, path.join(path.dirname(args.codexSkills), "skills-disabled", stamp, ".codex")),
      ...cleanDocsSkills(args.agentsSkills, path.join(path.dirname(args.codexSkills), "skills-disabled", stamp, ".agents")),
    );
  }

  for (const name of SKILLS) {
    const destination = path.join(args.codexSkills, name);
    installed[destination] = copyTree(path.join(sourceRoot, name), destination, path.join(backupRoot, ".codex"));
    codexInstalledDirs.push(destination);
  }

  const agentsDocsInit = path.join(args.agentsSkills, "docs-init");
  installed[agentsDocsInit] = copyTree(path.join(sourceRoot, "docs-init"), agentsDocsInit, path.join(backupRoot, ".agents"));

  const installedErrors = validateAll([...codexInstalledDirs, agentsDocsInit]);
  if (installedErrors.length > 0) {
    throw new InstallError(`Installed validation failed: ${installedErrors.join("; ")}`);
  }

  if (!args.keepLegacy) {
    disabled.push(...disableLegacy(args.codexSkills, path.join(path.dirname(args.codexSkills), "skills-disabled", stamp)));
  }

  console.log(JSON.stringify({
    installed,
    disabled,
    backup_root: backupRoot,
    codex_skills: args.codexSkills,
    agents_docs_init: agentsDocsInit,
    valid: true,
  }, null, 2));
}

try {
  main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(JSON.stringify({ error: message, valid: false }, null, 2));
  process.exit(1);
}
