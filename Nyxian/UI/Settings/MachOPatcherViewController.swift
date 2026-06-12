/*
 SPDX-License-Identifier: AGPL-3.0-or-later

 Copyright (C) 2025 - 2026 emexlab

 This file is part of Nyxian.

 Nyxian is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Nyxian is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Nyxian. If not, see <https://www.gnu.org/licenses/>.
*/

import UIKit

class MachOPatcherViewController: UIThemedTableViewController {
    var path: String
    var entitlements: PEEntitlement
    let applyHandler: () -> Void
    
    struct EntitlementRow {
        let title: String
        let detail: String
        let flag: PEEntitlement
    }

    struct EntitlementSection {
        let title: String
        let rows: [EntitlementRow]
    }

    private let sections: [EntitlementSection] = [
        EntitlementSection(title: NSLocalizedString("Task & Process Access", comment: ""), rows: [
            EntitlementRow(title: NSLocalizedString("Get Task Allowed", comment: ""), detail: "Allows other entitled processes to obtain the process's task port.", flag: .getTaskAllowed),
            EntitlementRow(title: NSLocalizedString("Task for Pid", comment: ""), detail: "Allows obtaining the task port of other processes by pid.", flag: .taskForPid),
            EntitlementRow(title: NSLocalizedString("Process Enumeration", comment: ""), detail: "Allows listing all running processes in nyxian.", flag: .processEnumeration),
        ]),
        EntitlementSection(title: NSLocalizedString("Process Control", comment: ""), rows: [
            EntitlementRow(title: NSLocalizedString("Process Kill", comment: ""), detail: "Allows sending signals to other processes.", flag: .processKill),
            EntitlementRow(title: NSLocalizedString("Process Spawn", comment: ""), detail: "Allows spawning arbitrary processes.", flag: .processSpawn),
            EntitlementRow(title: NSLocalizedString("Process Spawn (Signed Only)", comment: ""), detail: "Spawn is restricted to signed binaries only.", flag: .processSpawnSignedOnly),
            EntitlementRow(title: NSLocalizedString("Process Elevate", comment: ""), detail: "Allows elevating ucred privileges.", flag: .processElevate),
            EntitlementRow(title: NSLocalizedString("Inherit Entitlements on Spawn", comment: ""), detail: "Child processes inherites the parent processes entitlements.", flag: .processSpawnInheriteEntitlements),
        ]),
        EntitlementSection(title: NSLocalizedString("Launch Services", comment: ""), rows: [
            EntitlementRow(title: NSLocalizedString("Start Service", comment: ""), detail: "Allows starting launch services. (unimplemented)", flag: .launchServicesStart),
            EntitlementRow(title: NSLocalizedString("Stop Service", comment: ""), detail: "Allows stopping launch services. (unimplemented)", flag: .launchServicesStop),
            EntitlementRow(title: NSLocalizedString("Toggle Service", comment: ""), detail: "Allows toggling launch services on or off. (unimplemented)", flag: .launchServicesToggle),
            EntitlementRow(title: NSLocalizedString("Get Service Endpoint", comment: ""), detail: "Allows reading the endpoint of a launch service.", flag: .launchServicesGetEndpoint),
            EntitlementRow(title: NSLocalizedString("Set Service Endpoint", comment: ""), detail: "Allows overriding the endpoint of a launch service that is not registerd.", flag: .launchServicesSetEndpoint),
        ]),
        EntitlementSection(title: NSLocalizedString("Host & Credentials", comment: ""), rows: [
            EntitlementRow(title: NSLocalizedString("Host Manager", comment: ""), detail: "Grants overriding host properties such as hostname.", flag: .hostManager),
            EntitlementRow(title: NSLocalizedString("Credentials Manager", comment: ""), detail: "Allows managing users and groups. (unimplemented)", flag: .credentialsManager),
        ]),
        EntitlementSection(title: NSLocalizedString("Security & Runtime", comment: ""), rows: [
            EntitlementRow(title: NSLocalizedString("Platform Process", comment: ""), detail: "Marks the process as a platform process.", flag: .platform),
            EntitlementRow(title: NSLocalizedString("Platform Root", comment: ""), detail: "Starts a process that is platformized as root user, meant as a security feature to prevent privelege escalations.", flag: .platformRoot),
            EntitlementRow(title: NSLocalizedString("DYLD Hide LiveProcess", comment: ""), detail: "Hides the PEProcesses trampoline process loader.", flag: .dyldHideLiveProcess),
        ]),
    ]

    init(machOPath path: String, applyHandler: @escaping () -> Void) {
        self.path = path
        self.entitlements = PEContainer.shared().entitlementForExecutable(atPath: path)
        self.applyHandler = applyHandler
        super.init(style: .insetGrouped)
    }

    @MainActor required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "\((path as NSString).lastPathComponent)'s Entitlements"
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "EntitlementCell")
        let barButton = UIBarButtonItem()
        barButton.title = NSLocalizedString("Apply", comment: "")
        barButton.target = self
        barButton.action = #selector(applyTapped)
        navigationItem.rightBarButtonItem = barButton
    }

    override func numberOfSections(in tableView: UITableView) -> Int {
        sections.count
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        sections[section].rows.count
    }

    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        sections[section].title
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "EntitlementCell", for: indexPath)
        let row = sections[indexPath.section].rows[indexPath.row]
        
        cell.textLabel?.text = row.title
        cell.detailTextLabel?.text = row.detail
        cell.selectionStyle = .none
        
        if cell.detailTextLabel == nil {
            let subtitleCell = UITableViewCell(style: .subtitle, reuseIdentifier: nil)
            subtitleCell.textLabel?.text = row.title
            subtitleCell.detailTextLabel?.text = row.detail
            subtitleCell.detailTextLabel?.textColor = .secondaryLabel
            subtitleCell.detailTextLabel?.numberOfLines = 2
            subtitleCell.selectionStyle = .none
            let toggle = makeToggle(for: row, indexPath: indexPath)
            subtitleCell.accessoryView = toggle
            return subtitleCell
        }
        
        cell.detailTextLabel?.text = row.detail
        cell.detailTextLabel?.textColor = .secondaryLabel
        cell.detailTextLabel?.numberOfLines = 2
        
        let toggle = makeToggle(for: row, indexPath: indexPath)
        cell.accessoryView = toggle
        
        return cell
    }
    
    
    override func tableView(_ tableView: UITableView, willDisplay cell: UITableViewCell, forRowAt indexPath: IndexPath) {
        cell.detailTextLabel?.numberOfLines = 2
    }
    
    override func tableView(_ tableView: UITableView, estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat { 60 }
    override func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        UITableView.automaticDimension
    }

    private func makeToggle(for row: EntitlementRow, indexPath: IndexPath) -> UISwitch {
        let toggle = UIThemedSwitch()
        toggle.isOn = entitlements.contains(row.flag)
        toggle.tag = indexPath.section * 1000 + indexPath.row   // encode position
        toggle.addTarget(self, action: #selector(toggleChanged(_:)), for: .valueChanged)
        return toggle
    }

    @objc private func toggleChanged(_ sender: UISwitch) {
        let sectionIndex = sender.tag / 1000
        let rowIndex = sender.tag % 1000
        let flag = sections[sectionIndex].rows[rowIndex].flag

        if sender.isOn {
            entitlements.insert(flag)
        } else {
            entitlements.remove(flag)
        }
    }
    
    @objc private func applyTapped() {
        PEContainer.shared().setEntitlements(entitlements, forExecutableAtPath: path)
        self.applyHandler()
        self.dismiss(animated: true)
    }
}
