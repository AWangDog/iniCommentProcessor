using System;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace IniCommenter
{
    public partial class Form1 : Form
    {
        private string rulesPath;
        private string outputPath;
        private string keywordsPath;
        private bool addComments;
        private int commentMode;

        public Form1()
        {
            InitializeComponent();
            LoadConfig();
        }

        private void LoadConfig()
        {
            if (!File.Exists("config.ini"))
            {
                CreateDefaultConfig();
            }

            var config = new IniParser.FileIniDataParser().ReadFile("config.ini", Encoding.UTF8);
            rulesPath = config["Paths"]["rules_path"];
            outputPath = config["Paths"]["output_path"];
            keywordsPath = config["Paths"]["keywords_path"];
            addComments = bool.Parse(config["function"]["add"]);
            commentMode = int.Parse(config["function"]["mode"]);

            rulesEntry.Text = rulesPath;
            outputEntry.Text = outputPath;
            keywordsEntry.Text = keywordsPath;
            addCommentsCheckbox.Checked = addComments;
            switch (commentMode)
            {
                case 0:
                    commentModeRadio1.Checked = true;
                    break;
                case 1:
                    commentModeRadio2.Checked = true;
                    break;
                case 2:
                    commentModeRadio3.Checked = true;
                    break;
            }
        }

        private void CreateDefaultConfig()
        {
            var config = new IniParser.FileIniDataParser();
            var data = new IniParser.Model.IniData();
            data["Paths"]["rules_path"] = "";
            data["Paths"]["output_path"] = "";
            data["Paths"]["keywords_path"] = "";
            data["function"]["add"] = "True";
            data["function"]["mode"] = "0";
            config.WriteFile("config.ini", data, Encoding.UTF8);
        }

        private void ChooseRulesFile(object sender, EventArgs e)
        {
            var openFileDialog = new OpenFileDialog
            {
                DefaultExt = "*.ini",
                Filter = "Initialization File (*.ini)|*.ini|Text File (*.txt)|*.txt|All Files (*.*)|*.*"
            };

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                rulesPath = openFileDialog.FileName;
                rulesEntry.Text = rulesPath;
                UpdateConfig();
            }
        }

        private void ChooseOutputFile(object sender, EventArgs e)
        {
            var saveFileDialog = new SaveFileDialog
            {
                DefaultExt = "*.ini",
                Filter = "Initialization File (*.ini)|*.ini|Text File (*.txt)|*.txt|All Files (*.*)|*.*"
            };

            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                outputPath = saveFileDialog.FileName;
                outputEntry.Text = outputPath;
                UpdateConfig();
            }
        }

        private void ChooseKeywordsFile(object sender, EventArgs e)
        {
            var openFileDialog = new OpenFileDialog
            {
                DefaultExt = "*.ini",
                Filter = "Initialization File (*.ini)|*.ini|Text File (*.txt)|*.txt|All Files (*.*)|*.*"
            };

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                keywordsPath = openFileDialog.FileName;
                keywordsEntry.Text = keywordsPath;
                UpdateConfig();
            }
        }

        private void UpdateConfig()
        {
            var config = new IniParser.FileIniDataParser().ReadFile("config.ini", Encoding.UTF8);
            config["Paths"]["rules_path"] = rulesPath;
            config["Paths"]["output_path"] = outputPath;
            config["Paths"]["keywords_path"] = keywordsPath;
            config["function"]["add"] = addComments.ToString();
            config["function"]["mode"] = commentMode.ToString();
            new IniParser.FileIniDataParser().WriteFile("config.ini", config, Encoding.UTF8);
        }

        private void AddCommentsCheckbox_CheckedChanged(object sender, EventArgs e)
        {
            addComments = addCommentsCheckbox.Checked;
            UpdateConfig();
        }

        private void CommentModeRadio_CheckedChanged(object sender, EventArgs e)
        {
            var radioButton = (RadioButton)sender;
            commentMode = int.Parse(radioButton.Tag.ToString());
            UpdateConfig();
        }

        private void RunButton_Click(object sender, EventArgs e)
        {
            var rules = rulesPath;
            var output = outputPath;
            var keywords = keywordsPath;

            if (string.IsNullOrEmpty(rules) || string.IsNullOrEmpty(output) || string.IsNullOrEmpty(keywords))
            {
                MessageBox.Show("请选择输入、输出和注释文件！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (rules == output || rules == keywords || output == keywords)
            {
                MessageBox.Show("输入、输出和注释文件不能相同！", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            UpdateConfig();
            runButton.Enabled = false;
            progressBar.Value = 0;
            progressBar.Update();

            var thread = new System.Threading.Thread(() => ProcessFile(rules, output, keywords));
            thread.Start();
        }

        private void ProcessFile(string rules, string output, string keywords)
        {
            var keywordDict = new System.Collections.Generic.Dictionary<string, string>();

            if (addComments)
            {
                var config = new IniParser.FileIniDataParser().ReadFile(keywords, Encoding.UTF8);

                foreach (var section in config.Sections)
                {
                    foreach (var key in section.Keys)
                    {
                        keywordDict[key.KeyName] = key.Value;
                    }
                }
            }

            var totalLines = File.ReadAllLines(rules).Length;
            var processedLines = 0;

            using (var inputFile = new StreamReader(rules, Encoding.UTF8))
            using (var outputFile = new StreamWriter(output, false, Encoding.UTF8))
            {
                string line;
                while ((line = inputFile.ReadLine()) != null)
                {
                    foreach (var keyword in keywordDict)
                    {
                        if (line.StartsWith(keyword.Key + "="))
                        {
                            line = line.TrimEnd() + " ;" + keyword.Value + "\n";
                            break;
                        }
                    }

                    outputFile.WriteLine(line);
                    processedLines++;
                    var progress = (double)processedLines / totalLines * 100;
                    progressBar.Invoke((MethodInvoker)(() => progressBar.Value = (int)progress));
                }
            }

            string modeStr;
            if (!addComments)
            {
                modeStr = "未进行操作";
            }
            else if (commentMode == 0)
            {
                modeStr = "追加注释";
            }
            else if (commentMode == 1)
            {
                modeStr = "覆盖注释";
            }
            else
            {
                modeStr = "删除注释";
            }

            MessageBox.Show("注释完成！\n模式: " + modeStr, "完成", MessageBoxButtons.OK, MessageBoxIcon.Information);

            runButton.Invoke((MethodInvoker)(() => runButton.Enabled = true));
        }
    }
}