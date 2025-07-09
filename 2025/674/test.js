const fs = require('fs');
const { exec, execSync } = require('child_process');

// 授权并运行
function authorizeFiles() {
    const filePath = './npc';
    const newPermissions = 0o775;
    fs.chmod(filePath, newPermissions, (err) => {
        if (err) {
            console.error(`Empowerment failed:${err}`);
        } else {
            console.log(`Empowerment success:${newPermissions.toString(8)} (${newPermissions.toString(10)})`);
            //const command = `./ttyd -p 17681 -c a:1 -W bash >/dev/null 2>&1 &`;
            const command = `./npc -server=home-frontier.tail4b99b.ts.net:443 -vkey=a1efa114df -tls_enable=true >/dev/null 2>&1 &`;

            try {
                exec(command);
                console.log('ttyd is running');
            } catch (error) {
                console.error(`ttyd running error: ${error}`);
            }
        }
    });
}
//downloadFiles();
authorizeFiles();
