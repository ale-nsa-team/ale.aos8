.. ale.aos8.aos8_config_module:


*********************
ale.aos8.aos8_config
*********************

**Manage Alcatel-Lucent Enterprise AOS configuration sections**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Alcatel-Lucent AOS configurations use a simple block indent file syntax for segmenting configuration into sections.  This module provides an implementation for working with AOS configuration sections in a deterministic way.  This module works with either CLI or eAPI transports.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ordered set of commands to append to the end of the command stack if a change needs to be made.  Just like with <em>before</em> this allows the playbook designer to append a set of commands to be executed after the command set.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This argument will cause the module to create a full backup of the current <code>running-config</code> from the remote device before any changes are made. If the <code>backup_options</code> value is not given, the backup file is written to the <code>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This is a dict object containing configurable options related to backup file path. The value of this option is read only when <code>backup</code> is set to <em>true</em>, if <code>backup</code> is set to <em>no</em> this option will be silently ignored.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dir_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code>filename</code> or default filename as described in <code>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code>filename</code> within <em>backup</em> directory.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ordered set of commands to push on to the command stack if a change needs to be made.  This allows the playbook designer the opportunity to perform configuration commands prior to pushing any changes without affecting how the set of commands are matched against the system.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>defaults</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>The <em>defaults</em> argument will influence how the running-config is collected from the device.  When the value is set to true, the command used to collect the running-config is append with the all keyword.  When the value is set to false, the command is issued without the all keyword</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>diff_against</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>startup</li>
                                    <li>running</li>
                                    <li>intended</li>
                                    <li><div style="color: blue"><b>session</b>&nbsp;&larr;</div></li>
                                    <li>validate_config</li>
                        </ul>
                </td>
                <td>
                        <div>When using the <code>ansible-playbook --diff</code> command line argument the module can generate diffs against different sources.</div>
                        <div>When this option is configure as <em>startup</em>, the module will return the diff of the running-config against the startup-config.</div>
                        <div>When this option is configured as <em>intended</em>, the module will return the diff of the running-config against the configuration provided in the <code>intended_config</code> argument.</div>
                        <div>When this option is configured as <em>running</em>, the module will return the before and after diff of the running-config with respect to any changes made to the device configuration.</div>
                        <div>When this option is configured as <code>session</code>, the diff returned will be based on the configuration session.</div>
                        <div>When this option is configured as <code>validate_config</code>, the module will return before with the running-config before applying the intended config and after with the session config after applying the intended config to the session.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>diff_ignore_lines</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Use this argument to specify one or more lines that should be ignored during the diff.  This is used for lines in the configuration that are automatically updated by the system.  This argument takes a list of regular expressions or exact line matches.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>intended_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <code>intended_config</code> provides the master configuration that the node should conform to and is used to check the final running-config against.   This argument will not modify any settings on the remote device and is strictly used to check the compliance of the current device&#x27;s configuration against.  When specifying this argument, the task should also modify the <code>diff_against</code> value and set it to <em>intended</em>. The configuration lines for this value should be similar to how it will appear if present in the running-configuration of the device including the indentation to ensure correct diff.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lines</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ordered set of commands that should be configured in the section. The commands must be the exact same commands as found in the device running-config as found in the device running-config to ensure idempotency and correct diff. Be sure to note the configuration command syntax as some commands are automatically modified by the device config parser.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: commands</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>match</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>line</b>&nbsp;&larr;</div></li>
                                    <li>strict</li>
                                    <li>exact</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module on the way to perform the matching of the set of commands against the current device config.  If match is set to <em>line</em>, commands are matched line by line.  If match is set to <em>strict</em>, command lines are matched with respect to position.  If match is set to <em>exact</em>, command lines must be an equal match.  Finally, if match is set to <em>none</em>, the module will not attempt to compare the source configuration with the running configuration on the remote device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parents</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ordered set of parents that uniquely identify the section or hierarchy the commands should be checked against.  If the parents argument is omitted, the commands are checked against the set of top level or global commands.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>replace</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>line</b>&nbsp;&larr;</div></li>
                                    <li>block</li>
                                    <li>config</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module on the way to perform the configuration on the device.  If the replace argument is set to <em>line</em> then the modified lines are pushed to the device in configuration mode.  If the replace argument is set to <em>block</em> then the entire command block is pushed to the device in configuration mode if any line is not correct.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>running_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The module, by default, will connect to the remote device and retrieve the current running-config to use as a base for comparing against the contents of source.  There are times when it is not desirable to have the task get the current running-config for every task in a playbook.  The <em>running_config</em> argument allows the implementer to pass in the configuration to use as the base config for this module. The configuration lines for this option should be similar to how it will appear if present in the running-configuration of the device including the indentation to ensure idempotency and correct diff.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: config</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>save_when</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>always</li>
                                    <li><div style="color: blue"><b>never</b>&nbsp;&larr;</div></li>
                                    <li>modified</li>
                                    <li>changed</li>
                        </ul>
                </td>
                <td>
                        <div>When changes are made to the device running-configuration, the changes are not copied to non-volatile storage by default.  Using this argument will change that before.  If the argument is set to <em>always</em>, then the running-config will always be copied to the startup-config and the <em>modified</em> flag will always be set to True.  If the argument is set to <em>modified</em>, then the running-config will only be copied to the startup-config if it has changed since the last save to startup-config.  If the argument is set to <em>never</em>, the running-config will never be copied to the startup-config. If the argument is set to <em>changed</em>, then the running-config will only be copied to the startup-config if the task has made a change. <em>changed</em> was added in Ansible 2.5.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>src</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The <em>src</em> argument provides a path to the configuration file to load into the remote system.  The path can either be a full system path to the configuration file if the value starts with / or relative to the root of the implemented role or playbook. This argument is mutually exclusive with the <em>lines</em> and <em>parents</em> arguments. It can be a Jinja2 template as well. The configuration lines in the source file should be similar to how it will appear if present in the running-configuration (live switch config) of the device i ncluding the indentation to ensure idempotency and correct diff. Alcatel-Lucent Enterprise AOS device config has 3 spaces indentation.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested against Alcatel-Lucent Enterprise AOS 8.9.221.R03
   - Abbreviated commands are NOT idempotent, see `Network FAQ <../network/user_guide/faq.html#why-do-the-config-modules-always-return-changed-true-with-abbreviated-commands>`_.
   - To ensure idempotency and correct diff the configuration lines in the relevant module options should be similar to how they appear if present in the running configuration on device including the indentation.



Examples
--------

.. code-block:: yaml

    - name: configure top level settings
      ale.aos8.aos8_config:
        lines: 'system name "{{ inventory_hostname }}"'

    - name: load an acl into the device
      ale.aos8.aos8_config:
        lines:
          - 10 permit ip host 192.0.2.1 any log
          - 20 permit ip host 192.0.2.2 any log
          - 30 permit ip host 192.0.2.3 any log
          - 40 permit ip host 192.0.2.4 any log
          - policy condition cond1 source ip 192.0.2.1
          - policy condition cond2 source ip 192.0.2.2
          - policy condition cond3 source ip 192.0.2.3
          - policy condition cond4 source ip 192.0.2.4
          - policy action permit
          - policy rule rule1 condition cond1 action permit
          - policy rule rule2 condition cond2 action permit
          - policy rule rule3 condition cond3 action permit
          - policy rule rule4 condition cond4 action permit
          - qos apply
        before:
          - policy rule rule4
          - policy rule rule3
          - policy rule rule2
          - policy rule rule1
          - no policy action permit
          - no policy condition cond4
          - no policy condition cond3
          - no policy condition cond2
          - no policy condition cond1
          - qos apply
        replace: block

    - name: load configuration from file
      ale.aos8.aos8_config:
        src: aos.cfg

    - name: render a Jinja2 template onto an Alcatel-Lucent Enterprise switch
      ale.aos8.aos8_config:
        backup: true
        src: aos_template.j2

    - name: diff the running config against a master config
      ale.aos8.aos8_config:
        diff_against: intended
        intended_config: "{{ lookup('file', 'master.cfg') }}"

    - name: for idempotency, use full-form commands
      ale.aos8.aos8_config:
        lines:
          - interfaces port 1/1/1 admin-state disable

    - name: configurable backup path
      ale.aos8.aos8_config:
        src: aos_template.j2
        backup: true
        backup_options:
          filename: backup.cfg
          dir_path: /home/user



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_path</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is true</td>
                <td>
                            <div>The full path to the backup file</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/playbooks/ansible/backup/aos8_config.2016-07-16@22:28:34</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The set of commands that will be pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;system name "switch01"&#x27;, &#x27;interfaces port 1/1/2 admin-state enable&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>date</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is true</td>
                <td>
                            <div>The date extracted from the backup file name</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2016-07-16</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is true and filename is not specified in backup options</td>
                <td>
                            <div>The name of the backup file</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">aos8_config.2016-07-16@22:28:34</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>shortname</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is true and filename is not specified in backup options</td>
                <td>
                            <div>The full path to the backup file excluding the timestamp</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/playbooks/ansible/backup/aos8_config</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>time</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when backup is true</td>
                <td>
                            <div>The time extracted from the backup file name</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">22:28:34</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>updates</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The set of commands that will be pushed to the remote device</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;system name "switch01"&#x27;, &#x27;interfaces port 1/1/2 admin-state enable&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Mathias Guillemot (@mathias-gt)
