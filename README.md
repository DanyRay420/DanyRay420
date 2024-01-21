- 👋 Hi, I’m @DanyRay101
- 👀 I’m interested in ...Staying relevant. Only way to do that is stay up do date with new tech!
- 🌱 I’m currently learning ... about "."Machine auto learning, auto bots, create and deploy mass agents to go out a work that 9-5 for me while i play the bank! creating the best working agents to help automate my lifestyle, stay relevant. Creating Artificial intell to do the work for me. Training the best models in the world."." 
- 💞️ I’m looking to collaborate on ... Makeing the best trading bot known to human, you should see my private stock! 
- 📫 How to reach me ...  Danyray101@gmail.com


<^>oo<^>  ✨ special ✨ repository  <^>00<^>
You got Mail

// NOTE: This script was written by evandcoleman: https://github.com/evandcoleman/scriptable

class Cache {
  constructor(name) {
    this.fm = FileManager.iCloud();
    this.cachePath = this.fm.joinPath(this.fm.documentsDirectory(), name);

    if (!this.fm.fileExists(this.cachePath)) {
      this.fm.createDirectory(this.cachePath);
    }
  }
  async read(key, expirationMinutes) {
    try {
      const path = this.fm.joinPath(this.cachePath, key);
      await this.fm.downloadFileFromiCloud(path);
      const createdAt = this.fm.creationDate(path);

      if (expirationMinutes) {
        if ((new Date()) - createdAt > (expirationMinutes * 60000)) {
          this.fm.remove(path);
          return null;
        }
      }

      const value = this.fm.readString(path);

      try {
        return JSON.parse(value);
      } catch (error) {
        return value;
      }
    } catch (error) {
      return null;
    }
  }
  write(key, value) {
    const path = this.fm.joinPath(this.cachePath, key.replace('/', '-'));
    console.log(`Caching to ${path}...`);

    if (typeof value === 'string' || value instanceof String) {
      this.fm.writeString(path, value);
    } else {
      this.fm.writeString(path, JSON.stringify(value));
    }
  }
}

module.exports = Cache;